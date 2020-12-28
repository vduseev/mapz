"""Test merge method."""

from mapz.methods.merge import merge

import pytest


@pytest.fixture
def data():
    """Provide common dict structure for tests below."""

    return {
        "name": "Boris",
        "music": {"songs": ["Du Hast", "Du Hast - Live"]},
    }


@pytest.fixture
def data_to_merge_in():
    """Provide common structure to be merged in to the initial dict."""

    return {"name": "Duhast", "parental": "Vyacheslavovich"}


def test_merge(data, data_to_merge_in):
    """Test that merge properly overrides the fields.

    The 'name' should overwriten entirely. And a new field 'parental'
    gets to be added to the final merged structure.
    """

    merged = merge(data, data_to_merge_in)

    # Check name is overwritten.
    assert merged["name"] == "Duhast"
    # Check 'music' field is still there.
    assert merged["music"]["songs"][1] == "Du Hast - Live"
    # Check that new field has appeared.
    assert merged["parental"] == "Vyacheslavovich"
