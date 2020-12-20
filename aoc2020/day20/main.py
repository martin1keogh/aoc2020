from __future__ import annotations

from collections import namedtuple
from functools import lru_cache
from math import sqrt
from typing import List, Callable, Iterator, Optional, Iterable

from toolz import compose, identity, first, last, get_in

from aoc2020.shared.models import NoResultFoundException
from aoc2020.shared.parser_utils import groupwise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver

Tile = namedtuple("Tile", ["id", "top", "bottom", "left", "right"])


def tile_from_rows(id_: int, rows_iter: Iterator[str]) -> Tile:
    rows = list(rows_iter)
    top = rows[0]
    bottom = rows[-1]
    left = "".join(map(first, rows))
    right = "".join(map(last, rows))
    return Tile(id_, top, bottom, left, right)


@lru_cache(maxsize=None)
def vertical_flip(tile: Tile) -> Tile:
    return tile._replace(top=tile.bottom, bottom=tile.top, left=tile.left[::-1], right=tile.right[::-1])


@lru_cache(maxsize=None)
def horizontal_flip(tile: Tile) -> Tile:
    return tile._replace(top=tile.top[::-1], bottom=tile.bottom[::-1], left=tile.right, right=tile.left)


@lru_cache(maxsize=None)
def transpose(tile: Tile) -> Tile:
    return tile._replace(top=tile.left, left=tile.top, right=tile.bottom, bottom=tile.right)


transformations: List[Callable[[Tile], Tile]] = [
    identity,
    vertical_flip,
    horizontal_flip,
    compose(vertical_flip, horizontal_flip),
    transpose,
    compose(transpose, horizontal_flip),
    compose(transpose, vertical_flip),
]

# probably need a SolvedGrid type too
Grid = List[List[Optional[Tile]]]


class SolverDay20(Solver):
    puzzle: Puzzle[List[Tile]]

    @staticmethod
    def _explore_arrangement(grid: Grid, current_tile: int, to_go: List[Tile]) -> Iterator[Grid]:
        if not to_go:
            yield grid

        grid_size = len(grid)
        row = current_tile // grid_size
        column = current_tile % grid_size

        left: Optional[Tile] = get_in([row, column - 1], grid, default=None)
        above: Optional[Tile] = get_in([row - 1, column], grid, default=None)

        for i, tile in enumerate(to_go):
            for transformation in transformations:
                transformed_tile = transformation(tile)

                if above and not above.bottom == transformed_tile.top:
                    continue

                if left and not left.right == transformed_tile.left:
                    continue

                # local_grid = list(map(copy, grid))
                grid[row][column] = transformed_tile
                to_go_copy = to_go.copy()
                to_go_copy.pop(i)
                yield from SolverDay20._explore_arrangement(grid, current_tile + 1, to_go_copy)
            else:
                grid[row][column] = None

    def _solve(self) -> Grid:
        grid_size = int(sqrt(len(self.puzzle.data)))  # hopefully it's always a square
        empty_grid: Grid = [[None] * grid_size for _ in range(grid_size)]

        solution_gen = SolverDay20._explore_arrangement(empty_grid.copy(), 0, self.puzzle.data)
        for solution in solution_gen:
            return solution

        raise NoResultFoundException

    @staticmethod
    @groupwise_parser
    def parser(group: Iterable[str]) -> Tile:
        lines = list(group)
        return tile_from_rows(int(lines[0].split()[1][:-1]), iter(lines[1:]))

    def part1(self) -> int:
        solution = self._solve()
        return solution[0][0].id * solution[0][-1].id * solution[-1][0].id * solution[-1][-1].id  # type: ignore


if __name__ == '__main__':
    SolverDay20(PuzzleDownloader(day=20, parser=SolverDay20.parser).get_puzzle()).run()
