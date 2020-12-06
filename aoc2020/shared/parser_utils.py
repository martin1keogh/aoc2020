import functools
from itertools import groupby
from typing import Callable, TypeVar, List, Iterable

T = TypeVar("T")


def linewise_parser(parser: Callable[[str], T]) -> Callable[[str], List[T]]:
    @functools.wraps(parser)
    def wrap(*args: str) -> List[T]:
        return list(map(parser, args[-1].splitlines()))

    return wrap


def groupwise_parser(parser: Callable[[Iterable[str]], T]) -> Callable[[str], List[T]]:
    """Transform the parser so that it is called for each group (non-blank consecutive lines)"""
    @functools.wraps(parser)
    def wrap(*args: str) -> List[T]:
        lines = args[-1]
        # group together consecutive non-blank lines
        grouped = groupby(lines.splitlines(), lambda line: len(line) == 0)
        # parse each group individually, discarding the empty ones
        # (blank lines in the input, ie group separators)
        return [parser(group) for is_empty, group in grouped if not is_empty]

    return wrap
