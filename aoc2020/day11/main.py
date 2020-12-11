from __future__ import annotations

from dataclasses import field
from enum import Enum
from functools import lru_cache
from itertools import takewhile
from typing import List, Tuple, Iterator, Callable

from pydantic.dataclasses import dataclass

from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


class State(Enum):
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
            if not (0 <= xx < width and 0 <= yy < height):
                continue

            res.append((xx, yy))
    return res


def _gen(coord: Coord, direction: Tuple[int, int]) -> Iterator[Coord]:
    """Yields an infinite sequence of coordinates starting from `coord`, following `direction`"""
    x, y = coord
    x_move, y_move = direction
    while True:
        x += x_move
        y += y_move
        yield x, y


def _visible_from(coord: Coord, width: int, height: int) -> Iterator[Iterator[Coord]]:
    """Yields 8 iterators, each with all the positions reachable from `coord` using a straight line"""
    directions = [
        (1, 0), (1, 1), (0, 1), (-1, 1),
        (-1, 0), (-1, -1), (0, -1), (1, -1)
    ]
    for direction in directions:
        yield takewhile(
            lambda xy: 0 <= xy[0] < width and 0 <= xy[1] < height,
            _gen(coord, direction)
        )


@dataclass
class Layout:
    __root__: List[List[State]]
    _height: int = field(init=False)
    _width: int = field(init=False)

    def __post_init_post_parse__(self):
        self._height = len(self.__root__)
        self._width = len(self.__root__[0])

    def __hash__(self) -> int:
        return 0

    def __str__(self) -> str:
        # TODO clean this
        return "---\n" + "\n".join(map(", ".join, map(lambda l: map(str, l), self.__root__)))

    def __getitem__(self, xy: Coord) -> State:
        x, y = xy
        return self.__root__[y][x]

    def __setitem__(self, xy: Coord, value: State) -> None:
        x, y = xy
        self.__root__[y][x] = value

    def step_part1(self) -> Layout:
        new_layout = []

        for y, row in enumerate(self.__root__):
            new_row = []
            for x, position in enumerate(row):
                adj_seats = _adjacent_seats(x, y, self._width, self._height)
                if position == State.FREE and list(map(self.__getitem__, adj_seats)).count(State.TAKEN) == 0:
                    new_elem = "#"
                elif position == State.TAKEN and list(map(self.__getitem__, adj_seats)).count(State.TAKEN) >= 4:
                    new_elem = "L"
                else:
                    new_elem = position

                new_row.append(new_elem)
            new_layout.append(new_row)

        return Layout(__root__=new_layout)

    def step_part2(self) -> Layout:
        new_layout = []

        for y, row in enumerate(self.__root__):
            new_row = []
            for x, position in enumerate(row):
                taken_count = 0
                for visible_one_dir in _visible_from((x, y), self._width, self._height):
                    for visible_x, visible_y in visible_one_dir:
                        if self[visible_x, visible_y] == State.TAKEN:
                            taken_count += 1
                            break
                        if self[visible_x, visible_y] == State.FREE:
                            break

                if position == State.FREE and taken_count == 0:
                    new_elem = State.TAKEN
                elif position == State.TAKEN and taken_count >= 5:
                    new_elem = State.FREE
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

    def _solve_with(self, step: Callable[[Layout], Layout]) -> int:
        current = self.puzzle.data
        while True:
            new_layout = step(current)
            if new_layout == current:
                return sum([1 for row in current.__root__ for seat in row if seat == State.TAKEN])
            else:
                current = new_layout

    def part1(self) -> int:
        return self._solve_with(lambda layout: layout.step_part1())

    def part2(self) -> int:
        return self._solve_with(lambda layout: layout.step_part2())


if __name__ == '__main__':
    SolverDay11(PuzzleDownloader(day=11, parser=SolverDay11.parser).get_puzzle()).run()
