from mapz.modifiers.table import to_table

import pytest


@pytest.fixture
def data_map():
    return {
        "database": {
            "connection": {"host": "localhost", "port": 5432},
            "users": ["Duhast", "Valera"],
        }
    }


def test_simple(data_map):
    headers, rows = to_table(data_map)

    assert headers == ["Key", "Value"]
    assert rows == [
        ["database", ""],
        ["  connection", ""],
        ["    host", "localhost"],
        ["    port", "5432"],
        ["  users", str(data_map["database"]["users"])],
    ]


def test_limit(data_map):
    headers, rows = to_table(data_map, limit=3)

    assert rows == [
        ["database", ""],
        ["  connection", ""],
        ["    host", "localhost"],
        ["...", "..."],
    ]
