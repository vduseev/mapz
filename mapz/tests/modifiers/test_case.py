from functools import update_wrapper
from mapz.modifiers.case import to_lowercase, to_uppercase

import pytest


@pytest.fixture
def data_map():
    return {"Name": "Boris", "Data": {"songs": ["Du Hast", "Du Hast - Live"]}}


def test_lowercase(data_map):

    lowercase = to_lowercase(data_map)

    with pytest.raises(KeyError):
        lowercase["Name"]

    assert lowercase["name"] == "Boris"


def test_uppercase(data_map):

    to_uppercase(data_map, inplace=True)

    with pytest.raises(KeyError):
        data_map["Name"]

    assert data_map["NAME"] == "Boris"
