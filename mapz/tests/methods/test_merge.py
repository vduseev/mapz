from attr import dataclass
from mapz.methods.merge import merge

import pytest


@pytest.fixture
def data_map():
    return {"name": "Boris", "data": {"songs": ["Du Hast", "Du Hast - Live"]}}


@pytest.fixture
def merger():
    return {"name": "Duhast", "parental": "Vyacheslavovich"}


def test_merge(data_map, merger):

    merged = merge(data_map, merger)

    assert merged["name"] == "Duhast"
    assert merged["parental"] == "Vyacheslavovich"
