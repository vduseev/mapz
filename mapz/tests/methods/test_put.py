from mapz.methods.put import put

import pytest


@pytest.fixture
def data_map():
    return {"name": "Boris", "data": {"songs": ["Du Hast", "Du Hast - Live"]}}


def test_default(data_map):

    data = {}
    assert put(data, "name", "Duhast")["name"] == "Duhast"

    assert put(data_map, "name", "Duhast")["name"] == "Duhast"


def test_inverse(data_map):

    assert (
        put(data_map, "name", "Duhast", merge_inverse=True)["name"] == "Boris"
    )
