from mapz.methods.apply import apply

from typing import Mapping, MutableMapping, Union


def to_lowercase(
    data: Union[Mapping, MutableMapping], inplace=False, mapping_type=dict
):
    """Lowercase all string keys of the configuration"""

    return apply(
        data,
        modificator=lambda k, v, **kwargs: (
            k.lower() if isinstance(k, str) else k,
            v,
        ),
        inplace=inplace,
        mapping_type=mapping_type,
    )


def to_uppercase(
    data: Union[Mapping, MutableMapping], inplace=False, mapping_type=dict
):
    """Uppercase all string keys of the configuration"""

    return apply(
        data,
        modificator=lambda k, v, **kwargs: (
            k.upper() if isinstance(k, str) else k,
            v,
        ),
        inplace=inplace,
        mapping_type=mapping_type,
    )
