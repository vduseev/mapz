from typing import Callable, Hashable, List


SplitkeyModificatorCallable = Callable[[Hashable, List[str]], List[str]]


def splitkey(
    key: Hashable,
    prefix: str = "",
    sep: str = "_",
    modificator: SplitkeyModificatorCallable = lambda key, parts: parts,
) -> List[Hashable]:

    parts = [key]

    if isinstance(key, str):
        prefix = str(prefix)

        if key.startswith(prefix):
            key = key[len(prefix) :]
            parts = [key]

            if sep:
                if key.startswith(sep):
                    key = key[len(sep) :]
                if key.endswith(sep):
                    key = key[: -len(sep)]
                parts = [key]
                if sep in key:
                    parts = [p for p in key.split(sep) if p != ""]

        else:
            parts = []

    parts = modificator(key, parts)

    return parts
