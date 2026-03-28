import pytest
from helix.core.connectors.duckdb import DuckDB


@pytest.fixture
def db():
    con = DuckDB(path=":memory:")
    con.execute("CREATE TABLE test (id INTEGER, name VARCHAR)")
    con.execute("INSERT INTO test VALUES (1, 'alpha'), (2, 'beta')")
    yield con
    con.close()


def test_get_returns_dataframe(db):
    df = db.get("SELECT * FROM test")
    assert list(df.columns) == ["id", "name"]
    assert len(df) == 2


def test_get_filters_correctly(db):
    df = db.get("SELECT * FROM test WHERE id = 1")
    assert len(df) == 1
    assert df.iloc[0]["name"] == "alpha"


def test_execute_inserts_row(db):
    db.execute("INSERT INTO test VALUES (3, 'gamma')")
    df = db.get("SELECT * FROM test WHERE id = 3")
    assert len(df) == 1
    assert df.iloc[0]["name"] == "gamma"


def test_close_closes_connection(db):
    db.close()
    with pytest.raises(Exception):
        db.get("SELECT 1")
