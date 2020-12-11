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

    def __post_init_post_parse__(self) -> None:
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

    def apply_to_all_indices(self, f: Callable[[Coord], State]) -> Layout:
        new_layout = []

        for y in range(self._height):
            new_row = []
            for x in range(self._width):
                new_row.append(f((x, y)))
            new_layout.append(new_row)

        return Layout(__root__=new_layout)

    def state_updater_part1(self, coord: Coord) -> State:
        x, y = coord
        adj_seats = _adjacent_seats(x, y, self._width, self._height)
        current = self[x, y]
        if current == State.FREE and list(map(self.__getitem__, adj_seats)).count(State.TAKEN) == 0:
            return State.TAKEN
        elif current == State.TAKEN and list(map(self.__getitem__, adj_seats)).count(State.TAKEN) >= 4:
            return State.FREE
        else:
            return current

    def state_updater_part2(self, coord: Coord) -> State:
        x, y = coord
        current = self[x, y]
        taken_count = 0

        for visible_one_dir in _visible_from((x, y), self._width, self._height):
            for visible_x, visible_y in visible_one_dir:
                if self[visible_x, visible_y] == State.TAKEN:
                    taken_count += 1
                    break
                if self[visible_x, visible_y] == State.FREE:
                    break

        if current == State.FREE and taken_count == 0:
            return State.TAKEN
        elif current == State.TAKEN and taken_count >= 5:
            return State.FREE
        else:
            return current


class SolverDay11(Solver):
    puzzle: Puzzle[Layout]

    @staticmethod
    def parser(input_: str) -> Layout:
        return Layout(__root__=[list(row) for row in input_.splitlines()])  # type: ignore

    def _solve_with(self, step: Callable[[Layout], Callable[[Coord], State]]) -> int:
        current = self.puzzle.data
        while True:
            new_layout = current.apply_to_all_indices(step(current))
            if new_layout == current:
                return sum([1 for row in current.__root__ for seat in row if seat == State.TAKEN])
            else:
                current = new_layout

    def part1(self) -> int:
        return self._solve_with(lambda layout: layout.state_updater_part1)

    def part2(self) -> int:
        return self._solve_with(lambda layout: layout.state_updater_part2)


if __name__ == '__main__':
    SolverDay11(PuzzleDownloader(day=11, parser=SolverDay11.parser).get_puzzle()).run()
