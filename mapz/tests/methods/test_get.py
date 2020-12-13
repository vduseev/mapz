"""Test getter methods.

This module tests 2 main "get" methods of the library: ``getsert`` and ``get``.
"""

from typing import Any, Dict

from mapz.methods.get import get, getsert


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
    assert getsert(data, "key", True) == True
    assert data["key"] == True

    # data is not a valid dict, "key" cannot be in data,
    # default = False, so nothing should happend
    # and default should be returned.
    assert getsert(True, "key", False) is False


# Basic dict
d = {"name": "Duhast"}

# Basic list
l = [1, True, 4, {"a", "b"}, "text"]

# Nested dict, with list and dict
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
nd: Dict[str, Any] = dict(d)
nd["l"] = list(l) + [dict(d)]
nd["d"] = dict(d, l=list(l))

# Nested list, with dict and list
# [
#   [1, True, 4, {"a", "b"}, "text"],
#   1, True, 4, {"a", "b"}, "text",
#   { "name": "Duhast" }
# ]
nl = list(l)
nl.append(dict(d))
nl.insert(0, list(l))


def test_dict():
    """Test accessing items in dict."""

    # Existing, str key
    assert get(d, "name") == "Duhast"

    # Non-existing, str key
    assert get(d, "surname") is None

    # Non-existing, split str key
    assert get(d, "my.surname") is None
    assert get(d, "my.surname.is") is None

    # Non-existing, None key
    assert get(d, None) is None


def test_list():
    """Test accessing items in list."""

    # Existing, int key
    assert get(l, 1) == True

    # Existing, str key
    assert get(l, "0") == 1

    # Reverse, int key
    assert get(l, -1) == "text"

    # Reverse, str key
    assert get(l, "-2") == {"a", "b"}
    assert get(l, "-5") == 1

    # Reverse, out of bound, int key
    assert get(l, -6) is None

    # Reverse, out of bound, str key
    assert get(l, "-100000") is None


def test_list_wrong_key():
    """Test incorrectly accessing values in list."""

    assert get(l, "0s1") is None

    assert get(l, True) is None


def test_nested_dict():
    """Test accessing values in a nested dict."""

    # Existing, not nested, str key
    assert get(nd, "name") == "Duhast"

    # Existing, nested, str key
    assert get(nd, "l.2") == 4

    assert get(nd, "l.-2") == "text"

    assert get(nd, "l.-1.name") == "Duhast"

    assert get(nd, "d.l.1") == True


def test_nested_list():
    """Test accessing values in a nested list."""

    assert get(nl, 1) == True

    assert get(nl, "-1.name") == "Duhast"

    assert get(nl, "0.3") == {"a", "b"}


def test_wrong_data_type():
    """Test accessing values from a wrong data type."""

    assert get(True, "key") is None

    assert get(None, 1, False) == False
