import pandas as pd
import duckdb
from helix.core.connectors.base import Connector


MAIN_PATH = "/workspaces/helix/mock_data/db/helix.duckdb"


class DuckDB(Connector):

    def __init__(self, path: str = MAIN_PATH, read_only: bool = False):
        self._con = duckdb.connect(path, read_only=read_only)

    def get(self, query: str, **kwargs) -> pd.DataFrame:
        return self._con.execute(query, **kwargs).fetchdf()

    def execute(self, statement: str, **kwargs) -> None:
        self._con.execute(statement, **kwargs)

    def close(self):
        self._con.close()
