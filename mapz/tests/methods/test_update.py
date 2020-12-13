"""Test update method.

Update performs recursive/shallow update of one dictionary
with another.

TODO: test updating "brothers" with list instead of dict.
"""

from mapz.methods.update import update, Strategy

import pytest


@pytest.fixture
def data():
    """Provide shared data structure."""

    return {
        "name": "Duhast",
        True: False,
        "brothers": {"Kris": 36, "Mike": 29},
    }


def test_shallow(data):
    """Test shallow update."""

    # With shallow strategy "parental" key will get seccussfully added to
    # the dest mapping.
    update(data, {"parental": "Vyacheslavovich"}, Strategy.Shallow)
    assert data["name"] == "Duhast"
    assert data["parental"] == "Vyacheslavovich"

    # With shallow strategy "True" get gets successfully overwritten.
    update(data, {True: True}, Strategy.Shallow)
    assert data[True] is True

    # However, deeper and nested values are not explored, being instead
    # overwritten in their entirety.
    # As you can see below, whole content of "brothers" key was overwritten
    # instead of updating only "Kris"'s age.
    update(data, {"brothers": {"Kris": 48}}, Strategy.Shallow)
    assert data["brothers"] == {"Kris": 48}


def test_deep(data):
    """Test deep update."""

    # Unlike shallow strategy, default update strategy - deep - will
    # recursively look into nested objects to update them properly.
    update(data, {"brothers": {"Kris": 48}})
    assert data["brothers"] == {"Kris": 48, "Mike": 29}


def test_update_wrong_args():
    """Test update with wrong arguments."""

    # You cannot update None with True. And that would be an error in
    # mypy but "update" is coded in a way to return given object, so
    # it returns initial None.
    assert update(None, True) is None

    assert update([1, 2], [2, 3]) == [1, 2]

    assert update({1: 2}, True) == {1: 2}

    assert update(True, {1: 2}) is True
