from dataclasses import dataclass
from textwrap import dedent
from typing import List, Optional, TypeVar, Generic, Callable

from aoc2020.shared.puzzle import Puzzle
from aoc2020.shared.solver import Solver

T = TypeVar("T")


@dataclass(frozen=True)
class Example(Generic[T]):
    data: List[T]
    solution_part1: Optional[int] = None
    solution_part2: Optional[int] = None


class PuzzleExamplesChecker:
    day: int
    solver: Callable[[Puzzle], Solver]
    examples: List[Example]
    parser: Optional[Callable[[str], T]] = None

    def test_part1(self, example):
        solver_with_data = self.solver(Puzzle(day=self.day, data=self._parse_data(example.data)))
        assert solver_with_data.part1() == example.solution_part1

    def test_part2(self, example):
        solver_with_data = self.solver(Puzzle(day=self.day, data=self._parse_data(example.data)))
        assert solver_with_data.part2() == example.solution_part2

    def _parse_data(self, data: List[str]) -> List:
        if not self.parser:
            return data
        dedented = map(dedent, data)
        parsed = map(self.parser, dedented)
        return list(parsed)
