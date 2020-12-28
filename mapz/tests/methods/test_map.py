"""Test map function."""

from mapz.methods.map import map as zmap

import pytest


@pytest.fixture
def data():
    """Provide common data structure for tests below."""

    return {
        "name": "Boris",
        "music": {"songs": ["Du Hast", "Du Hast - Live"]},
    }


def modificator(k, v, **kwargs):
    """Modify string value by prepending it with '@'."""

    if isinstance(v, str):
        v = f"@{v}"
    return (k, v)


def test_apply(data):
    """Test applying modifying visitor."""

    modified = zmap(data, modificator)

    assert modified["name"] == "@Boris"
    assert data["name"] == "Boris"

    assert modified["music"]["songs"] == ["@Du Hast", "@Du Hast - Live"]
    assert data["music"]["songs"] == ["Du Hast", "Du Hast - Live"]


def test_apply_inplace(data):
    """Test applying modifying visitor in place."""

    zmap(data, modificator, inplace=True)

    assert data["name"] == "@Boris"

    assert data["music"]["songs"] == ["@Du Hast", "@Du Hast - Live"]


def test_default_modificator(data):
    """Test default map values that should not change anything."""

    assert zmap(data)["name"] == "Boris"
