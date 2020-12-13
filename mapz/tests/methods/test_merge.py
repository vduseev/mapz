from mapz.methods.merge import merge

import pytest


@pytest.fixture
def data():
    return {"name": "Boris", "data": {"songs": ["Du Hast", "Du Hast - Live"]}}


@pytest.fixture
def mergein():
    return {"name": "Duhast", "parental": "Vyacheslavovich"}


def test_merge(data, mergein):

    merged = merge(data, mergein)

    assert merged["name"] == "Duhast"
    assert merged["parental"] == "Vyacheslavovich"
