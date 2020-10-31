from .base import BaseMapz
from .methods import get as zget

from typing import Any, Hashable, List, MutableMapping, Union


class Mapz(BaseMapz):
    def __init__(self) -> None:
        super().__init__()

    def get(
        data: Union[MutableMapping, List],
        address: Hashable,
        sep: str = ".",
        default: Any = BaseMapz(),
    ):
        return zget(data, address, sep, default)
