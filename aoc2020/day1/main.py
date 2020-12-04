from dataclasses import dataclass
from itertools import combinations
from math import prod
from typing import ClassVar, List

from aoc2020.shared.models import NoResultFoundException
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


@dataclass
class SolverDay1(Solver):
    puzzle: Puzzle[List[int]]
    TARGET: ClassVar[int] = 2020

    def _solve_for(self, n: int) -> int:
        for x in combinations(self.puzzle.data, n):
            if sum(x) == self.TARGET:
                return prod(x)
        else:
            raise NoResultFoundException

    def part1(self) -> int:
        return self._solve_for(2)

    def part2(self) -> int:
        return self._solve_for(3)


def parser(string: str) -> List[int]:
    return list(map(int, string.splitlines()))


if __name__ == '__main__':
    SolverDay1(PuzzleDownloader(day=1, parser=parser).get_puzzle()).run()
