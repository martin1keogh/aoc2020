from dataclasses import dataclass
from math import prod
from typing import List, Literal, Callable, Dict

from pydantic import BaseModel, root_validator

from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


@dataclass
class Slope:
    down: int
    right: int


ForestSpot = Literal[".", "#"]


class Forest(BaseModel):
    __root__: List[List[ForestSpot]]

    @root_validator(pre=True)
    def _ensure_constant_width(cls, values: Dict) -> Dict:
        widths = map(len, values["__root__"])
        if len(set(widths)) != 1:
            raise ValueError("Non constant width found in forest.")
        return values

    @property
    def height(self) -> int:
        return len(self.__root__)

    @property
    def width(self) -> int:
        if not self.__root__:
            return 0
        return len(self.__root__[0])

    def path_to_end(self, slope: Slope) -> List[ForestSpot]:
        x, y = 0, 0
        visited_spots: List[ForestSpot] = []
        while y < self.height:
            visited_spots.append(self.__root__[y][x])
            y += slope.down
            x += slope.right
            x %= self.width
        return visited_spots


@dataclass
class SolverDay3(Solver):
    puzzle: Puzzle[Forest]

    def part1(self) -> int:
        path = self.puzzle.data.path_to_end(Slope(down=1, right=3))
        return path.count("#")

    def part2(self) -> int:
        slopes = [
            Slope(down=1, right=1),
            Slope(down=1, right=3),
            Slope(down=1, right=5),
            Slope(down=1, right=7),
            Slope(down=2, right=1),
        ]
        paths = map(self.puzzle.data.path_to_end, slopes)
        counts = map(lambda path: path.count("#"), paths)
        return prod(counts)

    @staticmethod
    def parser(string: str) -> Forest:
        by_line = string.splitlines()
        # using `list` directly in the map() makes mypy sad
        list_: Callable[[str], List[str]] = list
        by_character = map(list_, by_line)
        return Forest(__root__=list(by_character))


if __name__ == '__main__':
    SolverDay3(PuzzleDownloader(day=3, parser=SolverDay3.parser).get_puzzle()).run()
