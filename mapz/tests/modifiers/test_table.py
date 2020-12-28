"""Test to_table methods.

This module tests to_table method which turns Dict objects
into printable indented table.
"""

from mapz.modifiers.table import to_table

import pytest


@pytest.fixture
def data():
    """Provide reusable Dict-like structure for this test."""

    return {
        "database": {
            "connection": {"host": "localhost", "port": 5432},
            "users": ["Duhast", "Valera"],
        }
    }


def test_simple(data):
    """Test positive simple case.

    Includes:
        1. Nested dict objects and their fields
        2. List where each object receives a dash before value
    """

    headers, rows = to_table(data)

    assert headers == ["Key", "Value"]
    assert rows == [
        ["database", ""],
        ["  connection", ""],
        ["    host", "localhost"],
        ["    port", "5432"],
        ["  users", ""],
        ["    -", "Duhast"],
        ["    -", "Valera"],
    ]


def test_limit(data):
    """Test table print limit.

    In case below only 3 rows must be printed finished by
    an additional row indicating incomplete results.
    """

    _, rows = to_table(data, limit=3)

    assert rows == [
        ["database", ""],
        ["  connection", ""],
        ["    host", "localhost"],
        ["...", "..."],
    ]
