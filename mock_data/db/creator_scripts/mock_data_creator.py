import duckdb

# Connect to the persistent file (it creates it if it doesn't exist)
db = duckdb.connect("mock_data/helix_main.duckdb")

# You can now create multiple tables in this same connection
db.execute("CREATE TABLE IF NOT EXISTS rmbs_tapes AS SELECT * FROM ...")
db.execute("CREATE TABLE IF NOT EXISTS bwic_offers AS SELECT * FROM ...")
db.execute("CREATE TABLE IF NOT EXISTS macro_fred AS SELECT * FROM ...")

# List all tables in your database
print(db.execute("SHOW TABLES").fetchall())
