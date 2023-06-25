import typing as ty


def formatValue(value: int) -> str:
    # Can't use space directly as a separator, so `replace` is used
    return "{:,}\u2009₽".format(value).replace(",", "\u2009")


T = ty.TypeVar("T")


def unwrap(value: ty.Optional[T]) -> T:
    if value is None:
        raise RuntimeError("Unexpected None value")
    return value
