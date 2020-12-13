import pytest

from mapz.methods.copy import copy, deepcopy


@pytest.fixture
def data():
    return {"name": "Boris", "data": {"songs": ["Du Hast", "Du Hast - Live"]}}


def test_clone(data):

    cloned = copy(data)

    assert cloned["name"] == "Boris"

    assert cloned["data"]["songs"][0] == "Du Hast"

    data["data"]["songs"][0] = "Du Hast - Remix"

    assert cloned["data"]["songs"][0] == "Du Hast - Remix"


def test_deepclone(data):

    deepcloned = deepcopy(data)

    assert deepcloned["name"] == "Boris"

    assert deepcloned["data"]["songs"][0] == "Du Hast"

    data["data"]["songs"][0] = "Du Hast - Remix"

    assert deepcloned["data"]["songs"][0] == "Du Hast"
