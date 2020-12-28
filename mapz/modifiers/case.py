"""Case modifier. Changes keys of the given mapping structure.

Every method in this module essentially just applies a visitor function
to each key of the provided mapping structure. In case of the lowercase or
the uppercase functions such visitor correspondigly invokes "lower" or
"upper" python methods on string keys.

Hence, this module can be easily extended. For example, by adding a function
that transforms each key into a "Mocking Spongebob" meme text if we define
visitor function as:

    visitor = lambda k, v, **kwargs: (
        "".join([
            c.upper() if i % 2 else c.lower() for i, c in enumerate(a)
        ]) if isinstance(k, str) else k,
        v,
    )
"""

from typing import Any, Dict, Hashable, Mapping, Type, Union

from mapz.methods.map import map as zmap


def to_lowercase(
    mapping: Union[Dict[Hashable, Any], Mapping[Hashable, Any]],
    inplace: bool = False,
    mapping_type: Type[Dict[Hashable, Any]] = dict,
) -> Dict[Hashable, Any]:
    """Lowercase all string keys.

    Args:
        mapping: Mapping structure to transform.
        inplace (bool): If True, replace the given mapping structure with the
            newly generated lowercased Dict. Defaults to False. Only works
            when the given mapping is a mutable dict-like object.
        mapping_type (Type): Which type to use when creating a new lowercased
            structure. Defaults to ``dict``.

    Returns:
        Dict: Lowercased Dict-like structure with all string keys transformed
        to lowercase.
    """

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
    """Uppercase all string keys.

    Args:
        mapping: Mapping structure to transform.
        inplace (bool): If True, replace the given mapping structure with the
            newly generated uppercased Dict. Defaults to False. Only works
            when the given mapping is a mutable dict-like object.
        mapping_type (Type): Which type to use when creating a new uppercased
            structure. Defaults to ``dict``.

    Returns:
        Dict: Uppercase Dict-like structure with all string keys transformed
        to uppercase.
    """

    return zmap(
        mapping,
        visitor=lambda k, v, **kwargs: (
            k.upper() if isinstance(k, str) else k,
            v,
        ),
        inplace=inplace,
        mapping_type=mapping_type,
    )
