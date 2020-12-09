from mapz.methods.traverse import traverse

from typing import Hashable, Union, Mapping, MutableMapping, Dict, Any, cast


def to_dict(
    data: Union[Dict[Hashable, Any], Mapping[Hashable, Any]],
    inplace: bool = False,
) -> Dict[Hashable, Any]:

    d = traverse(data, mapping_type=dict)

    if isinstance(data, Dict) and inplace:
        data.clear()
        data.update(d)
        d = data

    # Explicit cast here because otherwise mypy complains that 'traverse' returns Any,
    # thus 'd' also evaluates to Any, and 'to_dict' returns Dict.
    return cast(Dict[Hashable, Any], d)
