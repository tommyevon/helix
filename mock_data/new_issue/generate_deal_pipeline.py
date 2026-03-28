"""
Generates synthetic ABS/MBS new issue deal pipeline data and writes it to DuckDB.

Columns mirror a typical DCM new issue monitor:
  deal     - Issuer + vintage identifier
  class    - Tranche rating/label (AAA, AA, A, BBB, etc.)
  size     - Tranche balance in $MM
  ipt      - Initial Price Talk (spread over SOFR, in bps, e.g. "S+165a")
  guidance - Revised guidance after book-building
  pricing  - Final cleared spread
  status   - Lifecycle stage of the deal
  notes    - Free-text commentary
"""

import random

import duckdb

random.seed(42)

# --- Synthetic deal universe ---

ISSUERS = [
    ("ACES", "Auto"),
    ("DRIVE", "Auto"),
    ("AMCAR", "Auto"),
    ("CARMX", "Auto"),
    ("NAROT", "Auto"),
    ("RALI", "Non-QM"),
    ("VERUS", "Non-QM"),
    ("SEMT", "Non-QM"),
    ("AOMT", "Non-QM"),
    ("CSMC", "Non-QM"),
    ("HALST", "CLO"),
    ("MIDO", "CLO"),
    ("TICP", "CLO"),
    ("MDPK", "CLO"),
    ("BXMT", "CRE"),
]

CLASSES = [
    ("A1", "AAA", 0.40),
    ("A2", "AAA", 0.20),
    ("B", "AA", 0.10),
    ("C", "A", 0.08),
    ("D", "BBB", 0.07),
    ("E", "BB", 0.05),
    ("F", "B", 0.04),
    ("G", "NR", 0.06),
]

STATUSES = ["Books Open", "Launched", "Priced", "Settled", "Withdrawn"]

STATUS_WEIGHTS = [0.10, 0.15, 0.35, 0.35, 0.05]

NOTES_POOL = [
    "3x oversubscribed at launch",
    "Tight concession vs. secondary",
    "Strong demand from money managers",
    "Anchor order from large insurance account",
    "Books covered within 2 hours",
    "Pricing inside IPT on strong book",
    "Widened from guidance on soft demand",
    "Withdrawn due to market volatility",
    "Priced flat to curve",
    "Significant APAC participation",
    "Deal upsized from $500MM at launch",
    "Guidance tightened 10bps on reverse inquiry",
    "Retained piece expected on F/G class",
    "B-piece sold to single buyer",
    "",
    "",
    "",  # blanks simulate missing notes
]


def _spread(base: int, tighten: int) -> str:
    """Format a SOFR spread string."""
    return f"S+{base}"


def _ipt_guidance_pricing(sector: str, cls_label: str) -> tuple[str, str, str]:
    """Generate realistic IPT → guidance → pricing tightening path."""
    base_spreads = {
        ("Auto", "AAA"): 55,
        ("Auto", "AA"): 90,
        ("Auto", "A"): 130,
        ("Auto", "BBB"): 180,
        ("Auto", "BB"): 310,
        ("Auto", "B"): 490,
        ("Auto", "NR"): 700,
        ("Non-QM", "AAA"): 135,
        ("Non-QM", "AA"): 185,
        ("Non-QM", "A"): 240,
        ("Non-QM", "BBB"): 325,
        ("Non-QM", "BB"): 475,
        ("Non-QM", "B"): 650,
        ("Non-QM", "NR"): 900,
        ("CLO", "AAA"): 140,
        ("CLO", "AA"): 195,
        ("CLO", "A"): 260,
        ("CLO", "BBB"): 355,
        ("CLO", "BB"): 525,
        ("CLO", "B"): 720,
        ("CLO", "NR"): 1000,
        ("CRE", "AAA"): 175,
        ("CRE", "AA"): 240,
        ("CRE", "A"): 310,
        ("CRE", "BBB"): 420,
        ("CRE", "BB"): 590,
        ("CRE", "B"): 775,
        ("CRE", "NR"): 1050,
    }
    base = base_spreads.get((sector, cls_label), 300)
    ipt_bps = base + random.randint(15, 30)
    guid_bps = base + random.randint(5, 15)
    price_bps = base + random.randint(-5, 5)
    return f"S+{ipt_bps}a", f"S+{guid_bps}", f"S+{price_bps}"


def generate_rows(n_deals: int = 30) -> list[dict]:
    rows = []
    years = [2023, 2024, 2025]
    for deal_num in range(1, n_deals + 1):
        issuer, sector = random.choice(ISSUERS)
        year = random.choice(years)
        seq = random.randint(1, 12)
        deal = f"{issuer} {year}-{seq}"
        status = random.choices(STATUSES, weights=STATUS_WEIGHTS, k=1)[0]

        # Total deal size $200MM–$2B
        deal_size_mm = random.randint(200, 2000)

        for cls_name, cls_label, pct in CLASSES:
            tranche_size = round(deal_size_mm * pct)
            if tranche_size < 5:
                continue

            ipt, guidance, pricing = _ipt_guidance_pricing(sector, cls_label)

            # Withdrawn deals have no pricing; Books Open may lack guidance
            if status == "Withdrawn":
                guidance = guidance
                pricing = "N/A"
            elif status == "Books Open":
                guidance = ""
                pricing = ""

            rows.append(
                {
                    "deal": deal,
                    "class": cls_name,
                    "size": tranche_size,
                    "ipt": ipt,
                    "guidance": guidance,
                    "pricing": pricing,
                    "status": status,
                    "notes": random.choice(NOTES_POOL),
                }
            )

    return rows


def main() -> None:
    rows = generate_rows(n_deals=30)

    db_path = "mock_data/deal_pipeline.duckdb"
    con = duckdb.connect(db_path)

    con.execute(
        """
        CREATE OR REPLACE TABLE deal_pipeline (
            deal     VARCHAR,
            class    VARCHAR,
            size     INTEGER,
            ipt      VARCHAR,
            guidance VARCHAR,
            pricing  VARCHAR,
            status   VARCHAR,
            notes    VARCHAR
        )
    """
    )

    con.executemany(
        "INSERT INTO deal_pipeline VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        [
            (
                r["deal"],
                r["class"],
                r["size"],
                r["ipt"],
                r["guidance"],
                r["pricing"],
                r["status"],
                r["notes"],
            )
            for r in rows
        ],
    )

    count = con.execute("SELECT COUNT(*) FROM deal_pipeline").fetchone()[0]
    print(f"Inserted {count} rows into {db_path}")

    preview = con.execute("SELECT * FROM deal_pipeline LIMIT 5").fetchall()
    for row in preview:
        print(row)
    con.close()


if __name__ == "__main__":
    main()
