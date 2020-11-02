from typing import Mapping
from mapz.methods.traverse import (
    traverse,
    isinstresult,
    iskwresult,
    issequence,
)


def test_issequence():

    assert issequence("") is False

    assert issequence(b"asd") is False

    assert issequence(bytes("asd", "utf-8")) is False


def test_iskwresult():

    assert iskwresult(None) is False

    assert iskwresult([1]) is False

    assert iskwresult((1,)) is False

    assert iskwresult((1, 2)) is True


def test_isinstresult():

    assert isinstresult(None) is False

    assert isinstresult((1,)) is True


duhast = {
    "person": {
        "name": "Duhast",
        "parental": "Vyacheslavovich",
        "songs": {
            "Du Hast (variations)": [
                {
                    "Du Hast - Live": {
                        "Wales": 2007,
                        "London": 2001,
                    }
                },
                "Du Hast - Remix",
            ]
        },
        "perks": ["awesome", ["vocal", "brave"]],
    },
    "event": b"Babaika Fest",
}


def test_immutable_traverse():
    def _on_kv(*args, **kwargs):
        k, v = args

        if issequence(v):
            v = "<list>"
        if isinstance(v, Mapping):
            v = "<dict>"

        kwargs["tracking_list"].append((k, v))

    visit_order = []

    traverse(duhast, func=_on_kv, tracking_list=visit_order)

    assert visit_order == [
        ("person", "<dict>"),
        ("name", "Duhast"),
        ("parental", "Vyacheslavovich"),
        ("songs", "<dict>"),
        ("Du Hast (variations)", "<list>"),
        (None, "<dict>"),
        ("Du Hast - Live", "<dict>"),
        ("Wales", 2007),
        ("London", 2001),
        (None, "Du Hast - Remix"),
        ("perks", "<list>"),
        (None, "awesome"),
        (None, "<list>"),
        (None, "vocal"),
        (None, "brave"),
        ("event", b"Babaika Fest"),
    ]


def test_mutable_traverse_copy_dict():

    assert traverse(duhast) == duhast


def test_immutable_traverse_plain_object():

    assert traverse(True) == True


def test_mutable_traverse_plain_object():

    assert traverse(True, lambda *args, **kwargs: 1 + 2) == True
