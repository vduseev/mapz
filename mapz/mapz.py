from mapz.modifiers.table import HeaderType
from mapz import methods, modifiers

from typing import (
    Any,
    Collection,
    Hashable,
    Iterable,
    Mapping,
    List,
    Dict,
    Optional,
    Tuple,
    Union,
)


class ProtoMapz(Dict[Hashable, Any]):
    pass


class Mapz(ProtoMapz):
    def __init__(self, *args: Mapping[Hashable, Any], **kwargs: Any) -> None:
        super().__init__()
        self.merge(*args, {k: v for k, v in kwargs.items()})

    def get(
        self,
        address: Hashable,
        default: Any = ProtoMapz(),
        sep: str = ".",
    ) -> Any:
        if type(default) == ProtoMapz:
            default = Mapz()

        return methods.get(
            data=self, address=address, default=default, sep=sep
        )

    def set(
        self,
        key: Hashable,
        val: Any,
        key_prefix: str = "",
        key_sep: str = ".",
        key_modificator: methods.SplitkeyModificatorCallable = lambda key, parts: parts,
        val_modificator: methods.TraverseModificatorCallable = lambda k, v, **kwargs: (
            k,
            v,
        ),
        merge_method: str = "recursive",
        merge_inverse: bool = False,
    ) -> Dict[Hashable, Any]:
        return methods.put(
            data=self,
            key=key,
            val=val,
            key_prefix=key_prefix,
            key_sep=key_sep,
            key_modificator=key_modificator,
            val_modificator=val_modificator,
            merge_method=merge_method,
            merge_inverse=merge_inverse,
            mapping_type=Mapz,
        )

    def update(  # type: ignore
        self,
        data: Mapping[Hashable, Any],
        method: str = "recursive",
    ) -> Dict[Hashable, Any]:
        # Intentionally incompatible with 'update' method of dict and MutableMapping.
        # The reason for is the requirement to return a Dict instead of None.
        # We want to be able to chain function calls via dot like this:
        #   my_map.to_lower().to_upper().update(this_dict).merge(whatever)
        # and it instantly violates return type of 'update' because for dict and
        # MutableMapping it must return None.
        # So, why bother with implementing compatibility with Iterable[Tuple[Any, Any]]
        # and **kwargs at all.
        # See mypy issue: https://github.com/python/mypy/issues/4250
        return methods.overwrite(
            dest=self,
            data=data,
            method=method,
        )

    def merge(
        self,
        *mappings: Mapping[Hashable, Any],
        key_prefix: str = "",
        key_sep: str = "__",
        merge_method: str = "recursive",
        merge_inverse: bool = False,
    ) -> Dict[Hashable, Any]:
        return methods.merge(
            self,
            *mappings,
            key_prefix=key_prefix,
            key_sep=key_sep,
            merge_method=merge_method,
            merge_inverse=merge_inverse,
            mapping_type=Mapz,
        )

    def submerge(
        self,
        *mappings: Mapping[Hashable, Any],
        key_prefix: str = "",
        key_sep: str = "__",
        merge_method: str = "recursive",
    ) -> Dict[Hashable, Any]:
        return methods.merge(
            self,
            *mappings,
            key_prefix=key_prefix,
            key_sep=key_sep,
            merge_method=merge_method,
            merge_inverse=True,
            mapping_type=Mapz,
        )

    def map(
        self,
        modificator: methods.TraverseModificatorCallable = lambda k, v, **kwargs: (
            k,
            v,
        ),
        inplace: bool = False,
        **kwargs: Any,
    ) -> Dict[Hashable, Any]:
        return methods.apply(
            data=self,
            modificator=modificator,
            inplace=inplace,
            mapping_type=Mapz,
            **kwargs,
        )

    def copy(self) -> Dict[Hashable, Any]:
        return methods.deepclone(self, mapping_type=Mapz)

    def lower(self, inplace: bool = False) -> Dict[Hashable, Any]:
        return modifiers.to_lowercase(
            self, inplace=inplace, mapping_type=Mapz
        )

    def upper(self, inplace: bool = False) -> Dict[Hashable, Any]:
        return modifiers.to_uppercase(
            self, inplace=inplace, mapping_type=Mapz
        )

    def flatten(
        self, prefix: str = "", sep: str = ".", inplace: bool = False
    ) -> Dict[Hashable, Any]:
        return modifiers.to_flat(
            self, prefix=prefix, sep=sep, inplace=inplace, mapping_type=Mapz
        )

    def to_dict(self, inplace: bool = False) -> Dict[Hashable, Any]:
        return modifiers.to_dict(self, inplace=inplace)

    def to_table(
        self,
        headers: modifiers.HeaderType = ["Key", "Value"],
        indentation: str = "  ",
        limit: int = 0,
    ) -> modifiers.TableType:
        return modifiers.to_table(
            self, headers=headers, indentation=indentation, limit=limit
        )

    def __getitem__(self, item: Hashable) -> Any:
        return self.get(item)

    def __getattr__(self, attr: str) -> Any:
        return self.get(attr)

    def __setitem__(self, item: Hashable, value: Any) -> None:
        self.set(item, value)

    def __setattr__(self, attr: str, value: Any) -> None:
        self.set(attr, value)

    def __copy__(self) -> Dict[Hashable, Any]:
        return methods.clone(self, mapping_type=Mapz)

    def __deepcopy__(
        self, memo: Optional[Dict[Hashable, Any]] = None
    ) -> Dict[Hashable, Any]:
        return methods.deepclone(self, mapping_type=Mapz)

    def __repr__(self) -> str:
        return f"MapZ{dict.__repr__(self)}"
