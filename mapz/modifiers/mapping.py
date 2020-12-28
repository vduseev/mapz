"""Mapping modifier. Transforms Dict like structure to dict."""

from typing import Any, Dict, Hashable, Mapping, Union, cast

from mapz.methods.traverse import traverse


def to_dict(
    mapping: Union[Dict[Hashable, Any], Mapping[Hashable, Any]],
    inplace: bool = False,
) -> Dict[Hashable, Any]:
    """Convert mapping structure to plain dict.

    This is useful to convert any subtype of ``dict`` back to its original
    form. For example, Mapz objects overwrite get/set methods of original
    dict to add new features. Applying ``to_dict`` to Mapz object will
    transform it into a simple dict with the same structure.

    Args:
        mapping: Mapping structure to convert.
        inplace (bool): Whether to replace given Dict with converted
            ``dict`` object. Only works if the passed ``mapping`` is
            also a mutable Dict-like object.

    Returns:
        dict: Plain dictionary object with the same structure. If the
        "inplace" is True, then the given "mapping" object is also
        rebound to newly converted dictionary instead of pointing to
        the initial given structure.

    Examples:
        Transform Mapz object to dict.

        >>> m = Mapz({"a": 1})
        >>> m
        MapZ{'a': 1}
        >>> to_dict(m)
        {'a': 1}
    """

    d = traverse(mapping, mapping_type=dict)

    if isinstance(mapping, Dict) and inplace:
        mapping.clear()
        mapping.update(d)
        d = mapping

    # Explicit cast here because otherwise mypy complains that 'traverse'
    # returns Any, thus 'd' also evaluates to Any, and 'to_dict'
    # returns Dict.
    # Somehow, unable to specify just 'dict' as a return type for this
    # function.
    return cast(Dict[Hashable, Any], d)
