""""""

from mapz.methods.set import set as zset

import pytest


@pytest.fixture
def data():
    return {"name": "Boris", "data": {"songs": ["Du Hast", "Du Hast - Live"]}}


def test_default(data):

    data = {}
    assert zset(data, "name", "Duhast")["name"] == "Duhast"

    assert zset(data, "name", "Duhast")["name"] == "Duhast"


def test_inverse(data):

    assert zset(data, "name", "Duhast", merge_inverse=True)["name"] == "Boris"
