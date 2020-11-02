import pytest

from mapz.methods.apply import apply


@pytest.fixture
def data_map():
    return {"name": "Boris", "data": {"songs": ["Du Hast", "Du Hast - Live"]}}


def modificator(*args, **kwargs):
    k, v = args
    if isinstance(v, str):
        v = f"@{v}"
    return (k, v)


def test_apply(data_map):

    modified = apply(data_map, modificator)

    assert modified["name"] == "@Boris"
    assert data_map["name"] == "Boris"

    assert modified["data"]["songs"] == ["@Du Hast", "@Du Hast - Live"]
    assert data_map["data"]["songs"] == ["Du Hast", "Du Hast - Live"]


def test_apply_inplace(data_map):

    apply(data_map, modificator, inplace=True)

    assert data_map["name"] == "@Boris"

    assert data_map["data"]["songs"] == ["@Du Hast", "@Du Hast - Live"]


def test_default_modificator(data_map):
    assert apply(data_map)["name"] == "Boris"
