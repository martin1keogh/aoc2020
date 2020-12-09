from collections import deque
from dataclasses import dataclass
from itertools import combinations
from typing import List

from aoc2020.shared.models import NoResultFoundException
from aoc2020.shared.parser_utils import linewise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


@dataclass
class SolverDay9(Solver):
    puzzle: Puzzle[List[int]]
    pool_size: int = 25

    @staticmethod
    @linewise_parser
    def parser(line: str) -> int:
        return int(line)

    def part1(self) -> int:
        pool = deque(self.puzzle.data[:self.pool_size])
        for next_number in self.puzzle.data[self.pool_size:]:
            if any(sum(combination) == next_number for combination in combinations(pool, 2)):
                pool.popleft()
                pool.append(next_number)
            else:
                return next_number
        raise NoResultFoundException

    def part2(self) -> int:
        target = self.part1()
        for length in range(2, len(self.puzzle.data)):
            for index in range(1, len(self.puzzle.data) - length):
                slice_ = self.puzzle.data[index:index+length]
                if sum(slice_) == target:
                    return min(slice_) + max(slice_)
        raise NoResultFoundException


if __name__ == '__main__':
    SolverDay9(PuzzleDownloader(day=9, parser=SolverDay9.parser).get_puzzle()).run()
