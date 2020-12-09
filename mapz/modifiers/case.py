from mapz.methods.apply import apply

from typing import Any, Dict, Hashable, Mapping, MutableMapping, Type, Union


def to_lowercase(
    data: Union[Dict[Hashable, Any], Mapping[Hashable, Any]],
    inplace: bool = False,
    mapping_type: Type[Dict[Hashable, Any]] = dict,
) -> Dict[Hashable, Any]:
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
    data: Union[Dict[Hashable, Any], Mapping[Hashable, Any]],
    inplace: bool = False,
    mapping_type: Type[Dict[Hashable, Any]] = dict,
) -> Dict[Hashable, Any]:
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
