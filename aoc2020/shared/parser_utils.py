import functools
from itertools import groupby
from typing import Callable, TypeVar, List

T = TypeVar("T")


def linewise_parser(parser: Callable[[str], T]) -> Callable[[str], List[T]]:
    @functools.wraps(parser)
    def wrap(*args: str) -> List[T]:
        return list(map(parser, args[-1].splitlines()))

    return wrap


def groupwise_parser(parser: Callable[[List[str]], T]) -> Callable[[str], List[T]]:
    @functools.wraps(parser)
    def wrap(*args: str) -> List[T]:
        lines = args[-1]
        groups: List[List[str]] = []
        grouped = groupby(lines.splitlines(), lambda line: len(line) == 0)

        for is_empty, group in grouped:
            if not is_empty:
                groups.append(list(group))

        return list(map(parser, groups))

    return wrap
