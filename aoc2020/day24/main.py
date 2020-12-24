from enum import Enum
from typing import List

from toolz import identity, groupby

from aoc2020.shared.parser_utils import linewise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


class Direction(Enum):
    E = (1, 0)
    W = (-1, 0)
    SE = (1, -1)
    SW = (0, -1)
    NE = (0, 1)
    NW = (-1, 1)

    def __init__(self, x: int, y: int):
        self.axis = (x, y)


class SolverDay24(Solver):
    puzzle: Puzzle

    @staticmethod
    @linewise_parser
    def parser(line_: str) -> List[Direction]:
        result = []
        buffer = ""
        for c in list(line_):
            if c in ["e", "w"]:
                result.append(Direction[(buffer + c).upper()])
                buffer = ""
            else:
                buffer = c
        return result

    def part1(self) -> int:
        to_flip = []
        for path in self.puzzle.data:
            to_append = (tuple(map(sum, (zip(*map(lambda direction: direction.axis, path))))))
            to_flip.append(to_append)

        count = 0
        for tile, flips in groupby(identity, to_flip).items():
            if len(flips) % 2 == 1:
                count += 1

        return count


if __name__ == '__main__':
    SolverDay24(PuzzleDownloader(day=24, parser=SolverDay24.parser).get_puzzle()).run()
