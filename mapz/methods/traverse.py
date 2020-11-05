from typing import (
    Any,
    Callable,
    List,
    MutableMapping,
    Sequence,
    Mapping,
    Tuple,
    Union,
)


TraverseModificatorCallable = Callable[..., Union[None, Tuple[Any, Any]]]
OrderingCallable = Callable[[Sequence], List]


# [not-sequence-types]
# These python types are not considered to be Sequences in ilexconf,
# even though, technically, they are Sequences in Python.
STR_TYPES = (str, bytes, bytearray)
# [not-sequence-types]


def issequence(arg: Any) -> bool:
    return isinstance(arg, Sequence) and not isinstance(arg, STR_TYPES)


def iskwresult(result: Any) -> bool:
    return (
        result is not None and isinstance(result, tuple) and len(result) == 2
    )


def isinstresult(result: Any) -> bool:
    return result is not None


def traverse(
    arg: Any,
    func: TraverseModificatorCallable = lambda *args, **kwargs: args,
    key_order: OrderingCallable = lambda keys: list(keys),
    list_order: OrderingCallable = lambda items: list(items),
    mapping_type=dict,
    **kwargs,
) -> Any:
    """Traverse any object recursively.

    We have to rely on the mapping type, because we can't safely determine it
    ourselves. ``traverse`` can be used by Mapz to transform ``dict`` objects
    however nested they might be into a ``Mapz`` object. That means repacking
    every nested dict into a different mapping type.
    Thus, we can't determine such mapping type from the ``arg`` and need to
    rely on the explicit declaration of it.

    Args:
        mapping_type (class): Type to pack mapping objects into. Defaults
            to ``dict``.
    """

    if "_depth" not in kwargs:
        kwargs["_depth"] = 0
    kwargs["_depth"] += 1

    result = None

    if isinstance(arg, Mapping):
        # This branch always returns mapping
        d = mapping_type()

        keys = key_order(arg.keys())
        for k in keys:
            v = arg[k]

            # At this point, ``func``` can transform both ``k`` and ``v``
            # to anything, even to None. Or turn ``v`` into a plain value.
            result = func(k, v, **kwargs)
            if iskwresult(result):
                k, v = result

            if isinstance(v, Mapping) or issequence(v):
                v = traverse(
                    v,
                    func,
                    key_order=key_order,
                    list_order=list_order,
                    mapping_type=mapping_type,
                    **kwargs,
                )

            dict.__setitem__(d, k, v)

        return d

    elif issequence(arg):
        # This branch always returns sequence of the same type as ``arg``.
        l = list()

        items = list_order(arg)
        for i in items:

            result = func(None, i, **kwargs)
            if iskwresult(result):
                k, i = result

            if isinstance(i, Mapping) or issequence(i):
                i = traverse(
                    i,
                    func,
                    key_order=key_order,
                    list_order=list_order,
                    mapping_type=mapping_type,
                    **kwargs,
                )

            l.append(i)

        t = type(arg)
        return t(l)

    else:
        # This branch returns whatever results we get from ``func`` or
        # ``arg`` itself if there were no results.
        result = func(None, arg, **kwargs)

        if iskwresult(result):
            k, v = result
            return v
        else:
            return arg
