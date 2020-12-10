from dataclasses import dataclass
from functools import lru_cache
from typing import List

from aoc2020.shared.parser_utils import linewise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver

Path = List[int]


@dataclass
class SolverDay10(Solver):
    puzzle: Puzzle[List[int]]

    @staticmethod
    @linewise_parser
    def parser(line: str) -> int:
        return int(line)

    def __hash__(self) -> int:
        return 1

    def __post_init__(self) -> None:
        self.puzzle.data.sort()

    def part1(self) -> int:
        current_joltage = 0
        one_diff_count = 0
        three_diff_count = 0
        for adapter in self.puzzle.data:
            if adapter - current_joltage == 1:
                one_diff_count += 1
            if adapter - current_joltage == 3:
                three_diff_count += 1
            current_joltage = adapter
        three_diff_count += 1  # built-in adapter
        return one_diff_count * three_diff_count

    @lru_cache(maxsize=None)
    def _count_path_to_end_from(self, index: int) -> int:
        """Returns the number of path from the value at `index` to the last value

        Reachable values are those within "3" jolts.
        This method assumes the self.puzzle.data list is sorted.
        """
        if index == len(self.puzzle.data) - 1:
            return 1

        next_indices = []
        for i, next_joltage in enumerate(self.puzzle.data[index + 1:index + 4]):
            if next_joltage <= self.puzzle.data[index] + 3:
                next_indices.append(i + index + 1)

        return sum(map(self._count_path_to_end_from, next_indices))

    def part2(self) -> int:
        start_points = []
        for i, joltage in enumerate(self.puzzle.data):
            if joltage <= 3:
                start_points.append(i)

        return sum(map(self._count_path_to_end_from, start_points))


if __name__ == '__main__':
    SolverDay10(PuzzleDownloader(day=10, parser=SolverDay10.parser).get_puzzle()).run()
