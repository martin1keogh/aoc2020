from __future__ import annotations

from dataclasses import field
from enum import Enum
from functools import lru_cache
from typing import List, Tuple

from pydantic.dataclasses import dataclass

from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


class Position(Enum):
    FLOOR = "."
    FREE = "L"
    TAKEN = "#"


Coord = Tuple[int, int]


@lru_cache(maxsize=None)
def _adjacent_seats(x: int, y: int, width: int, height: int) -> List[Coord]:
    res = []
    for xx in range(x - 1, x + 2):
        for yy in range(y - 1, y + 2):
            if xx == x and yy == y:
                continue
            if xx < 0 or yy < 0:
                continue
            if xx >= width or yy >= height:
                continue

            res.append((xx, yy))
    return res


@dataclass
class Layout:
    __root__: List[List[Position]]
    _height: int = field(init=False)
    _width: int = field(init=False)

    def __post_init_post_parse__(self):
        self._height = len(self.__root__)
        self._width = len(self.__root__[0])

    def __hash__(self) -> int:
        return 0

    def __str__(self) -> str:
        return "---\n" + "\n".join(map(", ".join, self.__root__))

    def __getitem__(self, xy: Coord) -> Position:
        x, y = xy
        return self.__root__[y][x]

    def __setitem__(self, xy: Coord, value: Position) -> None:
        x, y = xy
        self.__root__[y][x] = value

    def step_part1(self) -> Layout:
        new_layout = []

        for y, row in enumerate(self.__root__):
            new_row = []
            for x, position in enumerate(row):
                adj_seats = _adjacent_seats(x, y, self._width, self._height)
                if position == Position.FREE and list(map(self.__getitem__, adj_seats)).count(Position.TAKEN) == 0:
                    new_elem = "#"
                elif position == Position.TAKEN and list(map(self.__getitem__, adj_seats)).count(Position.TAKEN) >= 4:
                    new_elem = "L"
                else:
                    new_elem = position

                new_row.append(new_elem)
            new_layout.append(new_row)

        return Layout(__root__=new_layout)


class SolverDay11(Solver):
    puzzle: Puzzle[Layout]

    @staticmethod
    def parser(input_: str) -> Layout:
        return Layout(__root__=[list(row) for row in input_.splitlines()])

    def part1(self) -> int:
        current = self.puzzle.data
        while True:
            new_layout = current.step_part1()
            if new_layout == current:
                return sum([1 for row in current.__root__ for seat in row if seat == Position.TAKEN])
            else:
                current = new_layout


if __name__ == '__main__':
    SolverDay11(PuzzleDownloader(day=11, parser=SolverDay11.parser).get_puzzle()).run()
