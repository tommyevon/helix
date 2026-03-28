import duckdb
import pandas as pd


def get_database():
    db_path = "/workspaces/helix/mock_data/db/helix.duckdb"
    db = duckdb.connect(db_path, read_only=False)
    return db

def get_new_issue() -> pd.DataFrame:
    """
    Retrieve a sample of new issues from the deal pipeline database.
    Returns a limited set of records from the deal_pipeline table in the DuckDB
    database to provide a snapshot of recent deal pipeline data.
    Returns
    -------
    pd.DataFrame
        A DataFrame containing up to 10 records from the deal_pipeline table.
        The exact columns depend on the schema of the deal_pipeline table in
        the DuckDB database.
    Examples
    --------
    >>> df = get_new_issue()
    >>> df.shape
    (10, n_columns)
    >>> df.head()
    Notes
    -----
    The function opens a read-only connection to the DuckDB database located
    at '/workspaces/helix/mock_data/deal_pipeline.duckdb'. The connection is
    not explicitly closed; ensure proper resource management if calling this
    function repeatedly.
    """

    con = get_database()
    df = con.execute("SELECT * FROM deal_pipeline LIMIT 10").fetchdf()
    return df
