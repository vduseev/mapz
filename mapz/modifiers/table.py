from mapz.methods.traverse import traverse, TraverseModificatorCallable

from typing import Mapping, List


def to_table(
    data: Mapping,
    headers: List[str] = ["Key", "Value"],
    indentation: str = "  ",
    limit: int = 0,
):
    """Transform mapping into a table structure.

    Returns tuple of headers and rows.
    Returned structure is suitable for printing by Cleo library.
    """

    def modifier(k, v, _depth, rows, limit):
        if k is None:
            return k, v

        table_key = indentation * (_depth - 1) + k

        if not limit or limit and len(rows) < limit:
            value = ""
            if not isinstance(v, Mapping):
                s = " ".join(
                    str(v).replace("\n", " ").replace("\t", " ").split()
                )
                value = s if len(s) < 80 else f"{s[:76]}..."
            rows.append([table_key, value])

        return k, v

    rows = []
    traverse(
        data,
        func=modifier,
        key_order=lambda keys: sorted(keys),
        rows=rows,
        limit=limit,
    )

    if limit and len(rows) >= limit:
        rows.append(["...", "..."])

    return (headers, rows)
