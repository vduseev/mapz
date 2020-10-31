from typing import Mapping
from ilexconf.core.config import CoreConfig


def to_lowercase(data: Mapping, inplace=False):
    """Lowercase all string keys of the configuration"""
    return config.map(
        func=lambda k, v, **kwargs: (
            k.lower() if isinstance(k, str) else k,
            v,
        ),
        inplace=inplace,
    )


def to_uppercase(data: Mapping, inplace=False):
    """Uppercase all string keys of the configuration"""
    return data.map(
        func=lambda k, v, **kwargs: (
            k.upper() if isinstance(k, str) else k,
            v,
        ),
        inplace=inplace,
    )


def to_flat(data: Mapping, prefix: str = "", sep: str = "."):
    """Flatten the mapping so that there is no hierarchy."""

    d = dict()
    p = f"{prefix}{sep}" if prefix else ""
    for key in data:
        if isinstance(data[key], Mapping):
            flattened = to_flat(data[key], prefix=f"{p}{key}", sep=sep)
            d.update(flattened)
        else:
            d[f"{p}{key}"] = data[key]
    return d
