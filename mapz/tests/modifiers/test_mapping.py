from typing import Mapping
from mapz import Mapz
from mapz.modifiers.mapping import to_dict


def test_to_dict():
    d = {
        "database": {
            "host": "localhost",
            "port": 1234
        }
    }

    m = Mapz(d)

    cd = m.to_dict()

    def check_type(data):
        for k in data:
            if isinstance(data[k], Mapping):
                assert type(data[k]) == dict
                check_type(data[k])

    # Assert all nested mappigns are of dict type after conversion
    check_type(cd)

    # Same but inplace
    m.to_dict(inplace=True)
    check_type(m)    
