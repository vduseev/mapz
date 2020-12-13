import pytest

from mapz.methods.map import map as zmap


@pytest.fixture
def data():
    return {"name": "Boris", "data": {"songs": ["Du Hast", "Du Hast - Live"]}}


def modificator(*args, **kwargs):
    k, v = args
    if isinstance(v, str):
        v = f"@{v}"
    return (k, v)


def test_apply(data):

    modified = zmap(data, modificator)

    assert modified["name"] == "@Boris"
    assert data["name"] == "Boris"

    assert modified["data"]["songs"] == ["@Du Hast", "@Du Hast - Live"]
    assert data["data"]["songs"] == ["Du Hast", "Du Hast - Live"]


def test_apply_inplace(data):

    zmap(data, modificator, inplace=True)

    assert data["name"] == "@Boris"

    assert data["data"]["songs"] == ["@Du Hast", "@Du Hast - Live"]


def test_default_modificator(data):
    assert zmap(data)["name"] == "Boris"
