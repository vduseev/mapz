import pytest

from mapz.methods import get, getsert

# Basic dict
d = {"name": "Boris"}
# Basic list
l = [1, True, 4, {"a", "b"}, "text"]

# Nested dict, with list and dict
nd = dict(d)
nd["l"] = list(l) + [dict(d)]
nd["d"] = dict(d, l=list(l))

# Nested list, with dict and list
nl = list(l)
nl.append(dict(d))
nl.insert(0, list(l))


def test_dict():

    # Existing, str key
    assert get(d, "name") == "Boris"

    # Non-existing, str key
    assert get(d, "surname") is None

    # Non-existing, split str key
    assert get(d, "my.surname") is None
    assert get(d, "my.surname.is") is None

    # Non-existing, None key
    assert get(d, None) is None


def test_list():

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


def test_nested_dict():

    # Existing, not nested, str key
    assert get(nd, "name") == "Boris"

    # Existing, nested, str key
    assert get(nd, "l.2") == 4

    assert get(nd, "l.-2") == "text"

    assert get(nd, "l.-1.name") == "Boris"

    assert get(nd, "d.l.1") == True


def test_nested_list():

    assert get(nl, 1) == True

    assert get(nl, "-1.name") == "Boris"

    assert get(nl, "0.3") == {"a", "b"}
