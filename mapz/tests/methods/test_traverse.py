"""Test object traversal and help functions."""

from typing import Mapping

from mapz.methods.traverse import (
    iskvtuple,
    issequence,
    traverse,
)


def test_issequence():
    """Test correct non-byte sequence identification."""

    assert issequence("") is False

    assert issequence(b"asd") is False

    assert issequence(bytes("asd", "utf-8")) is False


def test_iskvtuple():
    """Test correct key-value tuple identification."""

    assert iskvtuple(None) is False

    assert iskvtuple([1]) is False

    assert iskvtuple((1,)) is False

    assert iskvtuple((1, 2)) is True


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
    """Test immutable traverse and visit order.

    This test verifies that my passing a non-modifying visitor
    function to the traversal method we are correctly visiting every
    node and do not alter the initial object.
    """

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
    """Test that plain traverse produces deep copy of the Dict."""

    duhast_traversed = traverse(duhast)
    assert duhast_traversed == duhast

    # Alter traversed version and verify the original
    # did not change.
    duhast_traversed["person"]["perks"][-1].append("valorian")
    len_traversed = len(duhast_traversed["person"]["perks"][-1])
    len_original = len(duhast["person"]["perks"][-1])
    assert len_traversed == len_original + 1


def test_immutable_traverse_plain_object():
    """Test that by traversin the plain object we get that object itself."""

    # Check on boolean
    assert traverse(True) is True

    # Check on integer
    assert traverse(5) == 5

    # Check non traversable class instance
    class NonTraversable:
        def __init__(self):
            self.value = [1, 2]

    t1 = NonTraversable()
    t2 = traverse(t1)

    # If traverse indeed could not traverse thorugh this
    # object and did not copy it but returned the original one
    # then both 't1' and 't2' point to the
    # same object.
    assert t1.value == t2.value

    # Alter the list value in the original object to make sure
    # the second object has the same change.
    t1.value.append(3)
    assert t2.value == [1, 2, 3]


def test_mutable_traverse_plain_object():
    """Test that modifying visitor function has no effect on plain objects."""

    assert traverse(True, lambda k, v, **kwargs: 1 + 2) is True
