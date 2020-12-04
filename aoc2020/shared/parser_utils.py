import functools
from typing import Callable, TypeVar, List

T = TypeVar("T")


def linewise_parser(parser: Callable[[str], T]) -> Callable[[str], List[T]]:
    @functools.wraps(parser)
    def wrap(*args: str) -> List[T]:
        return list(map(parser, args[-1].splitlines()))

    return wrap
