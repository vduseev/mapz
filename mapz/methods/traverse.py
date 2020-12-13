from typing import (
    Any,
    Callable,
    Hashable,
    List,
    Dict,
    Sequence,
    Mapping,
    Tuple,
    Type,
    Optional,
)
from mypy_extensions import Arg, KwArg


TraverseVisitorCallable = Callable[
    [Arg(Any, "k"), Arg(Any, "v"), KwArg(Any)], Optional[Tuple[Any, Any]]
]
OrderingCallable = Callable[[Sequence], List]


# [not-sequence-types]
# These python types are not considered to be Sequences in ilexconf,
# even though, technically, they are Sequences in Python.
STR_TYPES = (str, bytes, bytearray)
# [not-sequence-types]


def ismapping(arg: Any) -> bool:
    return isinstance(arg, Mapping)


def issequence(arg: Any) -> bool:
    return isinstance(arg, Sequence) and not isinstance(arg, STR_TYPES)


def iskvtuple(arg: Optional[Tuple[Any, ...]]) -> bool:
    return isinstance(arg, tuple) and len(arg) == 2


def traverse(
    arg: Any,
    visitor: TraverseVisitorCallable = lambda k, v, **kwargs: (k, v),
    key_order: OrderingCallable = lambda keys: list(keys),
    list_order: OrderingCallable = lambda items: list(items),
    mapping_type: Type[Dict[Hashable, Any]] = dict,
    **kwargs: Any,
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

    if "_index" not in kwargs:
        kwargs["_index"] = 0

    if "_ancestors" not in kwargs:
        kwargs["_ancestors"] = []
    else:
        # Have to clone ancestor list here, because otherwise the list
        # will share single instance between all traversals.
        # Instead, it should split into as many copies as needed. Each for
        # its own traversal path.
        kwargs["_ancestors"] = [a for a in kwargs["_ancestors"]] + [arg]

    result: Optional[Tuple[Any, ...]] = None

    if ismapping(arg):
        # This branch always returns mapping
        d = mapping_type()

        keys = key_order(arg.keys())
        for idx, k in enumerate(keys):
            v = arg[k]

            kwargs["_index"] = idx

            # At this point, ``func``` can transform both ``k`` and ``v``
            # to anything, even to None. Or turn ``v`` into a plain value.
            result = visitor(k, v, **kwargs)
            if result is not None and iskvtuple(result):
                k, v = result

            if ismapping(v) or issequence(v):
                v = traverse(
                    v,
                    visitor,
                    key_order=key_order,
                    list_order=list_order,
                    mapping_type=mapping_type,
                    **kwargs,
                )

            dict.__setitem__(d, k, v)

        return d

    elif issequence(arg):
        # This branch always returns sequence of the same type as ``arg``.
        l: List[Any] = list()

        items = list_order(arg)
        for idx, i in enumerate(items):

            kwargs["_index"] = idx

            result = visitor(None, i, **kwargs)
            if result is not None and iskvtuple(result):
                k, i = result

            if ismapping(i) or issequence(i):
                i = traverse(
                    i,
                    visitor,
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
        result = visitor(None, arg, **kwargs)

        if result is not None and iskvtuple(result):
            k, v = result
            return v
        else:
            return arg
