from dataclasses import dataclass
from typing import TypeVar

from aoc2020.shared.puzzle import Puzzle

T = TypeVar("T")


@dataclass
class Solver:
    puzzle: Puzzle[T]

    def part1(self) -> int:
        ...

    def part2(self) -> int:
        ...

    def run(self) -> None:
        print(f"Puzzle for {self.puzzle.day=}: solution for part 1: {self.part1()}, solution for part2: {self.part2()}")
