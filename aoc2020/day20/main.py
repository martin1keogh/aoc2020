from __future__ import annotations

from collections import namedtuple
from math import sqrt
from typing import List, Callable, Iterator, Optional, Iterable, Tuple, TypeVar, Set

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


T = TypeVar("T", List[str], Tile)


def vertical_flip(tile: T) -> T:
    if isinstance(tile, Tile):
        return tile._replace(top=tile.bottom, bottom=tile.top, left=tile.left[::-1], right=tile.right[::-1])
    else:
        return tile[::-1]


def horizontal_flip(tile: T) -> T:
    if isinstance(tile, Tile):
        return tile._replace(top=tile.top[::-1], bottom=tile.bottom[::-1], left=tile.right, right=tile.left)
    else:
        res = []
        for line in tile:
            res.append(line[::-1])
        return res


def transpose(tile: T) -> T:
    if isinstance(tile, Tile):
        return tile._replace(top=tile.left, left=tile.top, right=tile.bottom, bottom=tile.right)
    else:
        # https://stackoverflow.com/questions/6473679/transpose-list-of-lists
        return list(map("".join, zip(*tile)))


def crop(tile: List[str]) -> List[str]:
    res = tile[1:-1]
    res = map(lambda s: s[1:-1], res)
    return list(res)


transformations: List[Callable[[T], T]] = [
    identity,
    vertical_flip,
    horizontal_flip,
    compose(vertical_flip, horizontal_flip),
    transpose,
    compose(transpose, horizontal_flip),
    compose(transpose, vertical_flip),
]

# probably need a SolvedGrid type too
Grid = List[List[Optional[Tuple[Tile, Callable]]]]


class SolverDay20(Solver):
    puzzle: Puzzle[List[Tile]]

    @staticmethod
    def _explore_arrangement(grid: Grid, current_tile: int, to_go: List[Tile]) -> Iterator[Grid]:
        if not to_go:
            yield grid

        grid_size = len(grid)
        row = current_tile // grid_size
        column = current_tile % grid_size

        left: Optional[Tile] = get_in([row, column - 1, 0], grid, default=None)
        above: Optional[Tile] = get_in([row - 1, column, 0], grid, default=None)

        for i, tile in enumerate(to_go):
            for transformation in transformations:
                transformed_tile = transformation(tile)

                if above and not above.bottom == transformed_tile.top:
                    continue

                if left and not left.right == transformed_tile.left:
                    continue

                grid[row][column] = (transformed_tile, transformation)
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
        id_ = int(lines[0].split()[1][:-1])
        globals()[id_] = lines[1:]  # lol++
        return tile_from_rows(id_, iter(lines[1:]))

    def part1(self) -> int:
        solution = self._solve()
        return solution[0][0][0].id * solution[0][-1][0].id * solution[-1][0][0].id * solution[-1][-1][
            0].id  # type: ignore

    def part2(self) -> int:
        solution = list(zip(*self._solve()))  # guess it was wrong above too...
        image: List[List[List[str]]] = []

        for row in solution:
            row_image = []
            for (tile, transformation) in row:
                original = globals()[tile.id]
                transformed = transformation(original)
                transformed = transpose(
                    transformed)  # to get the same image as the example, should not be necessary I think?
                cropped = crop(transformed)
                row_image.append(cropped)
            image.append(row_image)

        s = []
        for row in image:
            for z in zip(*row):
                s.append("".join(z))

        monster_zones = set()
        for transformation in transformations:
            s = transformation(s)
            for y, row in enumerate(s):
                for x, _ in enumerate(row):
                    monsters = SolverDay20._detect_monster(s, x, y)
                    if monsters:
                        monster_zones.update(monsters)

            if monster_zones:
                break

        return sum(map(lambda l: l.count("#"), s)) - len(monster_zones)

    @staticmethod
    def _monster_shape() -> List[Tuple[int, int]]:
        s = """\
                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
        res = []
        for y, row in enumerate(s.splitlines()):
            for x, cell in enumerate(row):
                if cell == "#":
                    res.append((x, y))
        return res

    @staticmethod
    def _detect_monster(image: List[str], xx: int, yy: int) -> Optional[Set[Tuple[int, int]]]:
        adjusted = set(map(lambda t: (t[0] + xx, t[1] + yy), SolverDay20._monster_shape()))
        try:
            for x, y in adjusted:
                if not image[y][x] == "#":
                    return None
            return adjusted
        except IndexError:
            return None


if __name__ == '__main__':
    SolverDay20(PuzzleDownloader(day=20, parser=SolverDay20.parser).get_puzzle()).run()
