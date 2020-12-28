"""Test turning Dict objects into flat dictionaries.

Flat dictionary is a one level dictionary without nested
objects. Any list or non-byte sequence, however, violates that
rule and is not affected by flattening.
"""

from mapz.modifiers.flatten import to_flat

import pytest


@pytest.fixture
def data_map():
    """Provide reusable dictionary for tests."""

    return {
        "name": "Boris",
        "data": {"songs": ["Du Hast", "Du Hast - Live"]},
        "locations": [["town1", "town2", "town3"], {"birth": ["town4"]}],
    }


def test_default(data_map):
    """Test that nested dicts are transformed into multi-word keys."""

    flat = to_flat(data_map)

    assert flat["name"] == "Boris"
    assert flat["data.songs"] == data_map["data"]["songs"]
    assert list(flat.keys()) == ["name", "data.songs", "locations"]


def test_inplace(data_map):
    """Test that 'inplace' keywork modifies the original object."""

    to_flat(data_map, inplace=True)

    assert data_map["name"] == "Boris"
    assert data_map["data.songs"] == ["Du Hast", "Du Hast - Live"]
    assert list(data_map.keys()) == ["name", "data.songs", "locations"]
