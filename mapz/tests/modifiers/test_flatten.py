from mapz.modifiers.flatten import to_flat

import pytest


@pytest.fixture
def data_map():
    return {"name": "Boris", "data": {"songs": ["Du Hast", "Du Hast - Live"]}}


def test_default(data_map):

    flat = to_flat(data_map)

    assert flat["name"] == "Boris"
    assert flat["data.songs"] == data_map["data"]["songs"]
    assert list(flat.keys()) == ["name", "data.songs"]


def test_inplace(data_map):

    to_flat(data_map, inplace=True)

    assert data_map["name"] == "Boris"
    assert data_map["data.songs"] == ["Du Hast", "Du Hast - Live"]
    assert list(data_map.keys()) == ["name", "data.songs"]
