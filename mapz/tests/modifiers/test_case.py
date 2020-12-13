"""Test case modification of Dictionary keys."""

from mapz.modifiers.case import to_lowercase, to_uppercase

import pytest


@pytest.fixture
def data_map():
    """Provide reusable Dict structure for tests."""

    return {
        "Name": "Boris",
        "Data": {
            "songs": ["Du Hast", "Du Hast - Live", {"Surname": "Patches"}]
        },
    }


def test_lowercase(data_map):
    """Test that all keys are lowered."""

    lowercase = to_lowercase(data_map)

    with pytest.raises(KeyError):
        lowercase["Name"]

    assert lowercase["name"] == "Boris"
    assert lowercase["data"]["songs"][2]["surname"] == "Patches"


def test_uppercase(data_map):
    """Test that all keys converted to uppercase."""

    to_uppercase(data_map, inplace=True)

    with pytest.raises(KeyError):
        data_map["Name"]

    assert data_map["NAME"] == "Boris"
