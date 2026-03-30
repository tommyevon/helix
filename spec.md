# Project: Helix

**Vision:** A modular, high-performance structured credit analytics engine built with a "Clean Room" architecture. Designed for personal development using public/synthetic data, with a plug-and-play interface for enterprise data providers (Intex, Bloomberg, B-PIPE).

---

## 1. Technical Stack
* **Language:** Python 3.11+ (Strict Type Hinting)
* **API Framework:** FastAPI (Asynchronous execution)
* **Database:** DuckDB (In-process OLAP for loan-level analytics)
* **Frontend:** Streamlit (Rapid prototyping of financial dashboards)
* **Calculations:** NumPy / Pandas (Vectorized cashflow modeling)
* **Environment:** Linux DevContainer (Isolated sandbox)

---

## 2. Core Architecture: The Adapter Pattern
To ensure the transition from "Personal PoC" to "Enterprise Tool" is seamless, all data fetching must go through Abstract Base Classes (ABCs).

### **Data Providers**
1.  **MacroProvider (FRED):** Fetches SOFR, 10Y Treasuries, and HPI (House Price Index).
2.  **DealProvider (Mock/Intex):** Fetches deal structures, tranches, and waterfalls.
3.  **TapeProvider (Mock/SEC):** Fetches loan-level data (FICO, LTV, Note Rate, DTI).

---

## 3. Data Schema (The "Contract")
Claude must adhere to these schemas for all synthetic data generation.

### **Loan Tape Schema**
| Field | Type | Description |
| :--- | :--- | :--- |
| `loan_id` | String | Unique identifier |
| `orig_balance` | Float | Original Principal Balance |
| `curr_balance` | Float | Current Principal Balance |
| `fico` | Integer | Credit Score (300-850) |
| `ltv` | Float | Loan-to-Value Ratio (0-1.2) |
| `dti` | Float | Debt-to-Income Ratio |
| `note_rate` | Float | Annual Interest Rate |
| `state` | String | US State Code |

---

## 4. Analytics Engine Requirements
The engine must support "What-If" scenario analysis based on the following vectors:
* **Prepayment (CPR):** Conditional Prepayment Rate (0% to 50%).
* **Default (CDR):** Conditional Default Rate (0% to 20%).
* **Loss Severity:** Percentage of balance lost upon default (20% to 100%).
* **Servicing Lag:** Number of months between default and liquidation.

### **Waterfall Logic**
1.  **Interest Distribution:** Pay Senior Tranches first, then Mezzanine, then Subordinate.
2.  **Principal Distribution:** Sequential or Pro-Rata based on specific deal triggers (to be mocked).
3.  **Loss Allocation:** Reverse-sequential (bottom-up) allocation of realized losses.

---

## 5. Development Principles (For Claude Code)
* **Zero-Footprint:** Never use real firm data or PII.
* **TDD (Test-Driven Development):** Write the `pytest` for cashflow calculations before implementing the logic.
* **Performance:** Favor DuckDB SQL for loan-level aggregations over looping through Python lists.
* **Documentation:** Every function must have a docstring explaining the financial logic used.

---

## 6. Phase 1 Roadmap (PoC)
1.  [ ] **Scaffold:** Initialize directory structure and `CLAUDE.md`.
2.  [ ] **Mock Data:** Create a `SyntheticTapeGenerator` that produces 10k realistic Non-QM loans.
3.  [ ] **Macro Sync:** Implement `FredProvider` to pull current mortgage rates.
4.  [ ] **Cashflow Engine:** Build the core math for a single-tranche "Pass-Through" security.
5.  [ ] **Dashboard:** Launch a Streamlit app to visualize Yield-to-Maturity (YTM) vs. CDR/CPR vectors.