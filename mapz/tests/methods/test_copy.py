"""Test copying functions."""

from mapz.methods.copy import copy, deepcopy

import pytest


@pytest.fixture
def data():
    """Provide common test data structure."""

    return {"name": "Boris", "data": {"songs": ["Du Hast", "Du Hast - Live"]}}


def test_shallow_copy(data):
    """Test shallow copy."""

    cloned = copy(data)

    assert cloned["name"] == "Boris"

    assert cloned["data"]["songs"][0] == "Du Hast"

    data["data"]["songs"][0] = "Du Hast - Remix"

    assert cloned["data"]["songs"][0] == "Du Hast - Remix"


def test_deep_copy(data):
    """Test deep copy."""

    deepcloned = deepcopy(data)

    assert deepcloned["name"] == "Boris"

    assert deepcloned["data"]["songs"][0] == "Du Hast"

    data["data"]["songs"][0] = "Du Hast - Remix"

    assert deepcloned["data"]["songs"][0] == "Du Hast"
