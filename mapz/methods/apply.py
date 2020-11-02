from .traverse import traverse, TraverseModificatorCallable

from typing import Mapping, MutableMapping, Union


def apply(
    data: Union[Mapping, MutableMapping],
    modificator: TraverseModificatorCallable = lambda *args, **kwargs: args,
    inplace: bool = False,
    **kwargs
):
    mapping_type = type(data)

    d = traverse(data, modificator, mapping_type=mapping_type, **kwargs)

    if inplace:
        data.clear()
        data.update(d)
        d = data

    return d