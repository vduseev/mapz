import pytest

from mapz.methods.clone import clone, deepclone


@pytest.fixture
def data_map():
    return {"name": "Boris", "data": {"songs": ["Du Hast", "Du Hast - Live"]}}


def test_clone(data_map):

    cloned = clone(data_map)

    assert cloned["name"] == "Boris"

    assert cloned["data"]["songs"][0] == "Du Hast"

    data_map["data"]["songs"][0] = "Du Hast - Remix"

    assert cloned["data"]["songs"][0] == "Du Hast - Remix"


def test_deepclone(data_map):

    deep = deepclone(data_map)

    assert deep["name"] == "Boris"

    assert deep["data"]["songs"][0] == "Du Hast"

    data_map["data"]["songs"][0] = "Du Hast - Remix"

    assert deep["data"]["songs"][0] == "Du Hast"
