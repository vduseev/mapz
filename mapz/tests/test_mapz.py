from mapz.mapz import Mapz

import pytest


@pytest.fixture
def data():
    return {
        "databases": {
            "db1": {
                "host": "localhost",
                "port": 5432,
            },
        },
        "users": [
            "Duhast",
            "Valera",
        ],
        "Params": [
            {"ttl": 120, "flush": True},
            {frozenset({1, 2}): {1, 2}},
        ],
        "name": "Boris",
    }


def test_constructor(data):

    assert Mapz(data) == data

    assert Mapz({}, data, {}) == data

    assert Mapz(db__conn__host="1.2.3.4") == {
        "db": {"conn": {"host": "1.2.3.4"}}
    }


def test_get(data):

    m = Mapz(data)

    assert m["databases"]["db1"]["host"] == "localhost"
    assert m["databases.db1.host"] == "localhost"
    assert m.databases.db1.host == "localhost"

    assert m["databases"].db1.host == "localhost"
    assert m.databases["db1"].host == "localhost"
    assert m.databases.db1["host"] == "localhost"
    assert m["databases.db1"].host == "localhost"
    assert m.databases["db1.host"] == "localhost"


def test_get_nondefault(data):

    m = Mapz(data)

    assert m.get("nonexistent") == Mapz()
    assert m.get("theother", default=None) == None
    assert m.theother == Mapz()


def test_set(data):

    m = Mapz(data)

    m.set("users", ["Onotole"])
    assert m.users == ["Onotole"]

    m.set("databases.db1.host", {"direct": "1.2.3.4", "loop": "127.0.0.1"})
    assert m.databases.db1.host.loop == "127.0.0.1"

    assert (
        m.set(
            "databases_db1_host_loop", "172.0.0.1", key_sep="_"
        ).databases.db1.host.loop
        == "172.0.0.1"
    )


def test_set_item(data):

    m = Mapz(data)

    m["users"] = ["Onotole"]
    assert m.users == ["Onotole"]

    m["databases.db1.host"] = {"direct": "1.2.3.4", "loop": "127.0.0.1"}
    assert m.databases.db1.host.loop == "127.0.0.1"

    m["databases.db1.host.loop"] = "172.0.0.1"
    assert m.databases.db1.host.loop == "172.0.0.1"


def test_set_attr(data):

    m = Mapz(data)

    m.users = ["Onotole"]
    assert m.users == ["Onotole"]

    m.databases.db3.host.direct = "1.2.3.4"
    m.databases.db3.host.loop = "127.0.0.1"
    assert m.databases.db3.host.loop == "127.0.0.1"

    m.databases.db3.host.loop = "172.0.0.1"
    assert m.databases.db3.host.loop == "172.0.0.1"


def test_update(data):

    m = Mapz(data)

    assert m.update({"users": None}).users is None


def test_submerge(data):

    m = Mapz(data)

    m.submerge({"databases.db2.status": "OFF"}, key_sep=".")
    assert m.databases.db2.status == "OFF"


def test_shallow_copy(data):

    from copy import copy

    m = Mapz(data)
    shallow = copy(m)

    assert m.databases.db1.host == "localhost"
    m.databases.db1.host = "172.31.0.4"
    assert m.databases.db1.host == "172.31.0.4"
    assert shallow.databases.db1.host == "172.31.0.4"

    assert m.name == "Boris"
    m.name = "Dorian"
    assert m.name == "Dorian"
    assert shallow.name == "Boris"


def test_deep_copy(data):

    from copy import deepcopy

    m = Mapz(data)
    deep1 = deepcopy(m)
    deep2 = m.copy()

    assert m.databases.db1.port == 5432
    m.databases.db1.port = 1234
    assert m.databases.db1.port == 1234
    assert deep1.databases.db1.port == 5432
    assert deep2.databases.db1.port == 5432


def test_lower(data):

    m = Mapz(data)
    low = m.lower()

    assert m["Params.0.ttl"] == 120
    assert low["params.0.ttl"] == 120
    assert m.lower(inplace=True).params[0].ttl == 120


def test_upper(data):

    m = Mapz(data)
    up = m.upper()

    assert m.name == "Boris"
    assert up.NAME == "Boris"
    assert m.upper(inplace=True).NAME == "Boris"


def test_flatten(data):

    m = Mapz(data)
    flat = m.flatten(prefix="f_")

    assert flat.f_name == "Boris"
    assert flat["f_databases.db1.host"] == "localhost"


def test_map(data):
    def keypartswap(*args, **kwargs):
        k, v = args
        if k:
            k = str(k)
            l = len(k) // 2
            k = k[l:] + k[:l]

        return k, v

    m = Mapz(data)
    m.map(keypartswap, inplace=True)

    assert m.mena == "Boris"
    assert m.basesdata.b1d.stho == "localhost"

    result = m.map()

    m.basesdata.b1d.stho = "127.0.0.1"
    assert result.basesdata.b1d.stho == "localhost"
