from mapz.methods.map import map as zmap

from typing import Any, Dict, Hashable, Mapping, Type, Union


def to_lowercase(
    mapping: Union[Dict[Hashable, Any], Mapping[Hashable, Any]],
    inplace: bool = False,
    mapping_type: Type[Dict[Hashable, Any]] = dict,
) -> Dict[Hashable, Any]:
    """Lowercase all string keys of the configuration"""

    return zmap(
        mapping,
        visitor=lambda k, v, **kwargs: (
            k.lower() if isinstance(k, str) else k,
            v,
        ),
        inplace=inplace,
        mapping_type=mapping_type,
    )


def to_uppercase(
    mapping: Union[Dict[Hashable, Any], Mapping[Hashable, Any]],
    inplace: bool = False,
    mapping_type: Type[Dict[Hashable, Any]] = dict,
) -> Dict[Hashable, Any]:
    """Uppercase all string keys of the configuration"""

    return zmap(
        mapping,
        visitor=lambda k, v, **kwargs: (
            k.upper() if isinstance(k, str) else k,
            v,
        ),
        inplace=inplace,
        mapping_type=mapping_type,
    )
