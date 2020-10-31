from mapz.methods.getsert import getsert


def test_getsert():
    data = {}

    assert getsert(data, "key") is None

    assert getsert(data, "key", True) == True
    assert data["key"] == True

    assert getsert(True, "key", False) is False
