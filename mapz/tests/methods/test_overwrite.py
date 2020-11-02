from mapz.methods.overwrite import overwrite


def test_overwrite():

    dest = {"name": "Duhast", True: False}

    assert overwrite(dest, {"parental": "Vyacheslavovich"}, "overwrite") == {
        "name": "Duhast",
        "parental": "Vyacheslavovich",
        True: False,
    }

    assert overwrite(dest, {True: True}, "overwrite") == {
        "name": "Duhast",
        "parental": "Vyacheslavovich",
        True: True,
    }


def test_recursive():

    dest = {"person": {"name": "Duhast"}}

    assert overwrite(dest, {"person": {"parental": "Vyacheslavovich"}}) == {
        "person": {"name": "Duhast", "parental": "Vyacheslavovich"}
    }


def test_update_wrong_args():

    assert overwrite(None, True) is None

    assert overwrite([1, 2], [2, 3]) == [1, 2]

    assert overwrite({1: 2}, True) == {1: 2}

    assert overwrite(True, {1: 2}) == True
