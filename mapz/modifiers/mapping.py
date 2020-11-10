from mapz.methods.traverse import traverse

from typing import Union, Mapping, MutableMapping


def to_dict(
    data: Union[Mapping, MutableMapping], inplace=False
):
    """Lowercase all string keys of the configuration"""

    d = traverse(data)

    if inplace:
        data.clear()
        data.update(d)
        d = data

    return d
