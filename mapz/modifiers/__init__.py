"""Modifiers transform given mapping structures into something new.

For example, transform a dictionary into a printable table, flat structure,
plain dict object, or a dictionary with different keys.
"""

from .case import (  # noqa: F401
    to_lowercase as to_lowercase,
    to_uppercase as to_uppercase,
)
from .flatten import to_flat as to_flat  # noqa: F401
from .mapping import to_dict as to_dict  # noqa: F401
from .table import (  # noqa: F401
    HeaderType as HeaderType,
    RowType as RowType,
    TableType as TableType,
    to_table as to_table,
)
