from mapz.methods.update import update


def test_overwrite():

    dest = { "name": "Duhast", True: False }

    assert update(dest, { "parental": "Vyacheslavovich" }, "overwrite") == { "name": "Duhast", "parental": "Vyacheslavovich", True: False }

    assert update(dest, { True: True }, "overwrite") == { "name": "Duhast", "parental": "Vyacheslavovich", True: True }


def test_recursive():

    dest = { "person": { "name": "Duhast" } }

    assert update(dest, { "person": { "parental": "Vyacheslavovich" } }) == { "person": { "name": "Duhast", "parental": "Vyacheslavovich" } }


def test_update_wrong_args():
    
    assert update(None, True) is None

    assert update([1, 2], [2, 3]) == [1, 2]

    assert update({1: 2}, True) == {1: 2}

    assert update(True, {1: 2}) == True

