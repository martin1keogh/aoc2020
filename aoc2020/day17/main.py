from __future__ import annotations

import itertools
from dataclasses import dataclass
from typing import Iterator, Tuple, Set

from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver

Coord = Tuple[int, int, int, int]


@dataclass
class SmarterMultiverse:
    active_cells: Set[Coord]
    dimensions: Coord  # ~= max coordinates

    def __contains__(self, item: Coord) -> bool:
        for dim_item, dim_self in zip(item, self.dimensions):
            if not abs(dim_item) <= dim_self:
                return False
        return True

    def _neighbors(self, x: int, y: int, z: int, t: int) -> Iterator[Coord]:
        yield from (
            (xx, yy, zz, tt)
            for tt in range(t - 1, t + 2)
            for zz in range(z - 1, z + 2)
            for yy in range(y - 1, y + 2)
            for xx in range(x - 1, x + 2)
            if not (x == xx and y == yy and z == zz and t == tt)
            if (xx, yy, zz, tt) in self
        )

    def expand(self) -> SmarterMultiverse:
        return SmarterMultiverse(
            active_cells=self.active_cells.copy(),
            # 1.__add__ doesn't work :'(
            dimensions=tuple(map(lambda d: d + 1, self.dimensions))  # type: ignore
        )

    def run_cycle(self) -> SmarterMultiverse:
        new_universe = self.expand()
        (x, y, z, t) = new_universe.dimensions

        for (xx, yy, zz, tt) in itertools.product(
                range(-x, x + 1), range(-y, y + 1), range(-z, z + 1), range(-t, t + 1)
        ):
            active_neighbors = len(set(new_universe._neighbors(xx, yy, zz, tt)) & self.active_cells)
            cell_is_active = (xx, yy, zz, tt) in self.active_cells
            if not cell_is_active and active_neighbors == 3:
                new_universe.active_cells.add((xx, yy, zz, tt))
            elif cell_is_active and not (2 <= active_neighbors <= 3):
                new_universe.active_cells.remove((xx, yy, zz, tt))

        return new_universe


@dataclass
class BoringVerse(SmarterMultiverse):
    def expand(self) -> BoringVerse:
        return BoringVerse(
            active_cells=self.active_cells.copy(),
            # force the last dimension to 0
            dimensions=(self.dimensions[0] + 1, self.dimensions[1] + 1, self.dimensions[2] + 1, 0)
        )


class SolverDay17(Solver):
    puzzle: Puzzle[SmarterMultiverse]

    @staticmethod
    def parser(input_: str) -> SmarterMultiverse:
        cells = [list(row) for row in input_.splitlines()]

        dimensions = (len(cells[0]) // 2, len(cells) // 2, 0, 0)
        active = set()
        for y in range(len(cells)):
            for x in range(len(cells[0])):
                if cells[y][x] == "#":
                    active.add((x - len(cells[0]) // 2, y - len(cells) // 2, 0, 0))

        return SmarterMultiverse(active_cells=active, dimensions=dimensions)

    def part1(self) -> int:
        u = BoringVerse(active_cells=self.puzzle.data.active_cells, dimensions=self.puzzle.data.dimensions)
        for _ in range(6):
            # should fix it so that .run_cycle return self.type, but...
            u = u.run_cycle()  # type: ignore
        return len(u.active_cells)

    def part2(self) -> int:
        mu = self.puzzle.data
        for _ in range(6):
            mu = mu.run_cycle()
        return len(mu.active_cells)


if __name__ == '__main__':
    SolverDay17(PuzzleDownloader(day=17, parser=SolverDay17.parser).get_puzzle()).run()
