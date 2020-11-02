from mapz.methods.apply import apply

from typing import Mapping, MutableMapping, Union


def to_lowercase(data: Union[Mapping, MutableMapping], inplace=False):
    """Lowercase all string keys of the configuration"""

    return apply(
        data,
        modificator=lambda k, v, **kwargs: (
            k.lower() if isinstance(k, str) else k,
            v,
        ),
        inplace=inplace,
    )


def to_uppercase(data: Union[Mapping, MutableMapping], inplace=False):
    """Uppercase all string keys of the configuration"""

    return apply(
        data,
        modificator=lambda k, v, **kwargs: (
            k.upper() if isinstance(k, str) else k,
            v,
        ),
        inplace=inplace,
    )
