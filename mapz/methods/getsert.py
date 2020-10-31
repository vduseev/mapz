from typing import MutableMapping, Hashable, Any


def getsert(data: MutableMapping, key: Hashable, default: Any = None) -> Any:
    """Implements defaultdict feature."""

    if isinstance(data, MutableMapping):

        if key not in data:
            # Do not insert default value into data if it's None.
            if default is None:
                return default
            dict.__setitem__(data, key, default)
        return dict.__getitem__(data, key)

    else:

        return default
