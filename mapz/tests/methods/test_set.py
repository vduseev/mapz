"""Test set value function."""

from mapz.methods.set import set as zset

import pytest


@pytest.fixture
def data():
    """Provide common reusable data structure."""

    return {"name": "Boris", "data": {"songs": ["Du Hast", "Du Hast - Live"]}}


def test_default(data):
    """Test that simple set overwrite the key."""

    assert zset(data, "name", "Duhast")["name"] == "Duhast"


def test_inverse(data):
    """Test that inverse set does not overwrite the key."""

    assert zset(data, "name", "Duhast", inverse=True)["name"] == "Boris"
