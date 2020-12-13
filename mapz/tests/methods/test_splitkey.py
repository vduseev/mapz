"""Test key-splitting function."""

from mapz.methods.splitkey import splitkey


def test_non_str():
    """Test splitting non-string objects.

    Splitting should not occur.
    """

    assert splitkey(True) == [True]

    assert splitkey(frozenset({1, 2})) == [frozenset({1, 2})]


def test_str_noprefix_nosep_nomod():
    """Split strings without prefix and with default separator."""

    # No separator in value
    assert splitkey("name") == ["name"]

    # This value contains the separator
    assert splitkey("AWS_DEFAULT_REGION") == ["AWS", "DEFAULT", "REGION"]

    # No matter how many separators in the value there are
    # they will be accurately cut off.
    assert splitkey("my__name") == ["my", "name"]

    assert splitkey("__my_name__") == ["my", "name"]

    assert splitkey("___my__name__") == ["my", "name"]

    assert splitkey("____my__name") == ["my", "name"]


def test_str_prefix_nosep_nomod():
    """Split string based on given prefix and default separator."""

    assert splitkey("AWS_DEFAULT_REGION", prefix="AWS_") == [
        "DEFAULT",
        "REGION",
    ]

    assert splitkey("fish_users", prefix="fish_") == ["users"]

    assert splitkey("fish_users", prefix="fish") == ["users"]

    assert splitkey("fish_users", prefix="AWS") == []


def test_str_prefix_sep_nomod():
    """Split string based on given prefix and separator."""

    assert splitkey("AWS_DEFAULT_REGION", prefix="AWS", sep="_") == [
        "DEFAULT",
        "REGION",
    ]

    assert splitkey("AWS_DEFAULT_REGION", prefix="AWS_", sep="__") == [
        "DEFAULT_REGION"
    ]

    assert splitkey("__my_name", prefix="", sep="__") == ["my_name"]

    assert splitkey("__my_name", prefix="__", sep="") == ["my_name"]


def test_str_prefix_sep_mod():
    """Split string using given prefix, separator, and modificator.

    Modificator function is applied to split parts before returning
    the results.
    """

    def _modif(key, parts):
        return [p.lower() for p in parts]

    assert splitkey(
        "AWS_DEFAULT_REGION", prefix="AWS", sep="_", modificator=_modif
    ) == ["default", "region"]
