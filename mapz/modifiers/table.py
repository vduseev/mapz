"""Table modifier. Convert Dict to printable table.

This module implements a modifier that converts a dictionary like structure
to a printable table suitable for printing manually or using `Cleo's table
helpers`_, such as ``render_table``.

Types:
    RowType: Represents a single row consisting of strings.
    HeaderType: Represents a single header row consisting of strings.
    TableType: Represents a whole printable table structure.

.. _Cleo's table helpers:
   https://cleo.readthedocs.io/en/latest/helpers/table.html

"""

from typing import Any, Hashable, Iterable, List, Mapping, Optional, Tuple

from mapz.methods.traverse import (
    ismapping,
    issequence,
    traverse,
)


RowType = Iterable[str]
HeaderType = RowType
TableType = Tuple[HeaderType, Iterable[RowType]]


def to_table(
    mapping: Mapping[Hashable, Any],
    headers: Iterable[str] = ("Key", "Value"),
    indentation: str = "  ",
    limit: int = 0,
) -> TableType:
    """Transform dictionary into a printable table structure.

    Resulting table always consists of the two columns. The first column
    contains mapping keys sorted in ascending order from first row to last
    and indented according to the internal structure of the given mapping.

    If a key in the mapping represents another mapping or a list then the
    value across it in the "Value" column will be empty. If a key represents
    anything different, then its value will be cast to string and truncated
    if its length is more than 79 characters. In such case first 76
    characters of the value are taken and three dots ("...") indicating
    truncation are added to them.

    Each next nested level of the mapping is indented using the
    ``indentation`` string provided in the arguments.

    If a certain key contains a list of values, then each value printed in
    the following rows will be accompanied by the dash ("-") in the "Key"
    column. This also applied to the case when key contains a list of
    mappings. In such case the mappings will be printed as in YAML.

    If ``limit`` is > 0, then no more than ``limit`` rows will be converted.
    An additional row indicating truncation will be added as the last one
    (["...", "..."]).

    Args:
        mapping: Mapping or dictionary to transform to table.
        headers: Iterable of headers for the table. Defaults to
            ["Key", "Value"]
        indentation (str): String that will be used as an indentation of
            nested keys in the table. Defaults to double-space "  ".
        limit (int): Row limit. Limits the number of rows in the resulting
            table. Defaults to 0 (no limit).

    Returns:
        TableType: A tuple consiting of headers and list of rows.

    Examples:
        Below, a structure with nested values, dictionaries, plain lists,
        and lists of other dictionaries is transformed to a table. Notice
        how list items each get prepended by a dash and any nested key
        is indented.

        >>> m = Mapz({ \
                "databases": {
                    "db1": {
                        "host": "localhost",
                        "port": 5432,
                    },
                },
                "users": [
                    "Duhast",
                    "Valera",
                ],
                "Params": [
                    {"ttl": 120, "flush": True},
                    {frozenset({1, 2}): {1, 2}},
                ],
                "name": "Boris",
            })
        >>> to_table(m)
        (
            ['Key', 'Value'],
            [
                ['Params', ''],
                ['  - flush', 'True'],
                ['    ttl', '120'],
                ['  - frozenset({1, 2})', '{1, 2}'],
                ['databases', ''],
                ['  db1', ''],
                ['    host', 'localhost'],
                ['    port', '5432'],
                ['name', 'Boris'],
                ['users', ''],
                ['  -', 'Duhast'],
                ['  -', 'Valera']
            ]
        )

    """

    def builder(k: Any, v: Any, **kwargs: Any) -> Optional[Tuple[Any, Any]]:
        """Visit each key and value and collect them into row list.

        Args:
            **kwargs: Arguments provided by ``traverse`` function as well as
            by invoking function. Contains "_depth", "_index", and
            "_ancestors" values provided by ``traverse``. Must also contain
            "rows" and "limit" provided by function that invoked traverse.
        """

        # Mutable list of rows.
        rows = kwargs["rows"]
        # Limit of rows.
        limit = kwargs["limit"]
        # How deeply nested are we.
        depth = kwargs["_depth"]
        # Index of the current item (useful for processing lists).
        index = kwargs["_index"]
        # List of acenstors of current nested key/value.
        ancestors = kwargs["_ancestors"]

        # Render keys by default as:
        table_key = indentation * (depth - 1) + str(k)

        if (
            len(ancestors) > 1
            and ismapping(ancestors[-1])  # noqa: W503
            and issequence(ancestors[-2])  # noqa: W503
        ):
            # If node has two or more ancestors, then check if it's a
            # mapping within a list. Because in that case it must be
            # rendered as in YAML:
            # my_list
            #   - key1      value1
            #     key2      value2
            if index:
                table_key = indentation * (depth - 1) + str(k)
            else:
                table_key = indentation * (depth - 2) + "- " + str(k)

        elif ancestors and issequence(ancestors[-1]):
            # Render child items of lists as just a dash with proper indent
            table_key = indentation * (depth - 1) + "-"

        if not limit or limit and len(rows) < limit:

            value = ""
            if not (ismapping(v) or issequence(v)):
                s = " ".join(
                    str(v).replace("\n", " ").replace("\t", " ").split()
                )
                value = s if len(s) < 80 else f"{s[:76]}..."

            # Ignore empty lines with no key and no value.
            # Example: List of Mappings will result in such row.
            if not k and not value:
                return None

            rows.append([table_key, value])

        return None

    rows: List[RowType] = []
    traverse(
        mapping,
        visitor=builder,
        key_order=lambda keys: sorted(keys),
        rows=rows,
        limit=limit,
    )

    if limit and len(rows) >= limit:
        rows.append(["...", "..."])

    return (list(headers), rows)
