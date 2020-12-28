"""Test getter methods.

Test two main "get" methods of the library: ``getsert`` and ``get``.
"""

from typing import Any, Dict

from mapz.methods.get import get, getsert

import pytest


@pytest.fixture
def data():
    """Provide basic dict test structure."""

    return {"name": "Duhast"}


@pytest.fixture
def list_data():
    """Provide basic list structure for tests."""

    return [1, True, 4, {"a", "b"}, "text"]


@pytest.fixture
def nested_dict(data, list_data):
    """Provide nested dict, with list and dict."""

    # {
    #   "name": "Duhast",
    #   "l": [
    #       1, True, 4, {"a", "b"}, "text",
    #       {"name": "Duhast"}
    #   ],
    #   "d": {
    #       "name": "Duhast",
    #       "l": [1, True, 4, {"a", "b"}, "text"]
    #   }
    # }
    nd: Dict[str, Any] = dict(data)
    nd["l"] = list(list_data) + [dict(data)]
    nd["d"] = dict(data, l=list(list_data))
    return nd


@pytest.fixture
def nested_list(data, list_data):
    """Provide nested list, with dict and list."""

    # [
    #   [1, True, 4, {"a", "b"}, "text"],
    #   1, True, 4, {"a", "b"}, "text",
    #   { "name": "Duhast" }
    # ]
    nl = list(list_data)
    nl.append(dict(data))
    nl.insert(0, list(list_data))
    return nl


def test_getsert():
    """Test getsert method."""

    data = {}

    # data is valid dict, "key" does not exist in it,
    # but default = None, so function must return None
    # without inserting key=None into data.
    assert getsert(data, "key") is None
    assert "key" not in data

    # data is valid dict, "key" not in data, and
    # default = True, which should insert key=True
    # into data and return the resulting value
    assert getsert(data, "key", True) is True
    assert data["key"] is True

    # data is not a valid dict, "key" cannot be in data,
    # default = False, so nothing should happend
    # and default should be returned.
    assert getsert(True, "key", False) is False


def test_dict(data):
    """Test accessing items in dict."""

    # Existing, str key
    assert get(data, "name") == "Duhast"

    # Non-existing, str key
    assert get(data, "surname") is None

    # Non-existing, split str key
    assert get(data, "my.surname") is None
    assert get(data, "my.surname.is") is None

    # Non-existing, None key
    assert get(data, None) is None


def test_list(list_data):
    """Test accessing items in list."""

    # Existing, int key
    assert get(list_data, 1) is True

    # Existing, str key
    assert get(list_data, "0") == 1

    # Reverse, int key
    assert get(list_data, -1) == "text"

    # Reverse, str key
    assert get(list_data, "-2") == {"a", "b"}
    assert get(list_data, "-5") == 1

    # Reverse, out of bound, int key
    assert get(list_data, -6) is None

    # Reverse, out of bound, str key
    assert get(list_data, "-100000") is None


def test_list_wrong_key(list_data):
    """Test incorrectly accessing values in list."""

    assert get(list_data, "0s1") is None

    assert get(list_data, True) is None


def test_nested_dict(nested_dict):
    """Test accessing values in a nested dict."""

    # Existing, not nested, str key
    assert get(nested_dict, "name") == "Duhast"

    # Existing, nested, str key
    assert get(nested_dict, "l.2") == 4

    assert get(nested_dict, "l.-2") == "text"

    assert get(nested_dict, "l.-1.name") == "Duhast"

    assert get(nested_dict, "d.l.1") is True


def test_nested_list(nested_list):
    """Test accessing values in a nested list."""

    assert get(nested_list, 2) is True

    assert get(nested_list, "-1.name") == "Duhast"

    assert get(nested_list, "0.3") == {"a", "b"}


def test_wrong_data_type():
    """Test accessing values from a wrong data type."""

    assert get(True, "key") is None

    assert get(None, 1, False) is False
