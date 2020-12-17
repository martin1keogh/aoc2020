from __future__ import annotations

from collections import deque
from copy import deepcopy
from dataclasses import dataclass
from textwrap import dedent
from typing import Deque, Iterator

from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver

# mypy seems to get confused here, complains about "expected str, got Literal["#", "."]"
Cell = str  # Literal["#", "."]


@dataclass(frozen=True)
class Universe:
    cells: Deque[Deque[Deque[Cell]]]

    def __str__(self) -> str:
        layers = []
        for layer in self.cells:
            layers.append("\n".join(map("".join, layer)))
        layers_str = "\n-----\n".join(layers)
        s = f"""
+++++++++
{layers_str}
+++++++++
        """
        return dedent(s)

    def _neighbors(self, x: int, y: int, z: int) -> Iterator[Cell]:
        yield from (
            self.cells[zz][yy][xx]
            for zz in range(z - 1, z + 2) if 0 < zz < len(self.cells) - 1
            for yy in range(y - 1, y + 2) if 0 < yy < len(self.cells[0]) - 1
            for xx in range(x - 1, x + 2) if 0 < xx < len(self.cells[0][0]) - 1
            if not (x == xx and y == yy and z == zz)
        )

    def expand(self) -> Universe:
        new_universe = deepcopy(self)

        for layer in new_universe.cells:
            for row in layer:
                row.append(".")
                row.appendleft(".")
            empty_row = deque(["." for _ in range(len(row))])
            layer.append(empty_row.copy())
            layer.appendleft(empty_row.copy())
        empty_layer = deque([empty_row.copy() for _ in range(len(layer))])
        new_universe.cells.append(empty_layer)
        new_universe.cells.appendleft(deepcopy(empty_layer))

        return new_universe

    def run_cycle(self) -> Universe:
        new_universe = self.expand()
        copy_because_mutation = deepcopy(new_universe)

        for z, z_layer in enumerate(new_universe.cells):
            for y, y_layer in enumerate(z_layer):
                for x, cell in enumerate(y_layer):
                    active_neighbors = sum(1 for n in copy_because_mutation._neighbors(x, y, z) if n == "#")
                    if cell == "." and active_neighbors == 3:
                        new_universe.cells[z][y][x] = "#"
                    elif cell == "#" and not (2 <= active_neighbors <= 3):
                        new_universe.cells[z][y][x] = "."

        return new_universe


@dataclass(frozen=True, eq=True)
class Multiverse:
    cells: Deque[Deque[Deque[Deque[Cell]]]]

    def _neighbors(self, x: int, y: int, z: int, t: int) -> Iterator[Cell]:
        yield from (
            self.cells[tt][zz][yy][xx]
            for tt in range(t - 1, t + 2) if 0 < tt < len(self.cells) - 1
            for zz in range(z - 1, z + 2) if 0 < zz < len(self.cells[tt]) - 1
            for yy in range(y - 1, y + 2) if 0 < yy < len(self.cells[tt][zz]) - 1
            for xx in range(x - 1, x + 2) if 0 < xx < len(self.cells[tt][zz][yy]) - 1
            if not (x == xx and y == yy and z == zz and t == tt)
        )

    def expand(self) -> Multiverse:
        new_multiverse = deepcopy(self)

        for universe in new_multiverse.cells:
            for layer in universe:
                for row in layer:
                    row.append(".")
                    row.appendleft(".")
                empty_row = deque(["." for _ in range(len(row))])
                layer.append(empty_row.copy())
                layer.appendleft(empty_row.copy())
            empty_layer = deque([empty_row.copy() for _ in range(len(layer))])
            universe.append(empty_layer)
            universe.appendleft(deepcopy(empty_layer))
        empty_universe = deque([deepcopy(empty_layer) for _ in range(len(universe))])
        new_multiverse.cells.append(empty_universe)
        new_multiverse.cells.appendleft(deepcopy(empty_universe))

        return new_multiverse

    def run_cycle(self) -> Multiverse:
        new_universe = self.expand()
        copy_because_mutation = deepcopy(new_universe)

        for t, universe in enumerate(new_universe.cells):
            for z, z_layer in enumerate(universe):
                for y, y_layer in enumerate(z_layer):
                    for x, cell in enumerate(y_layer):
                        active_neighbors = sum(1 for n in copy_because_mutation._neighbors(x, y, z, t) if n == "#")
                        if cell == "." and active_neighbors == 3:
                            new_universe.cells[t][z][y][x] = "#"
                        elif cell == "#" and not (2 <= active_neighbors <= 3):
                            new_universe.cells[t][z][y][x] = "."

        return new_universe


class SolverDay17(Solver):
    puzzle: Puzzle[Universe]

    @staticmethod
    def parser(input_: str) -> Universe:
        rows = input_.splitlines()
        cells = deque([deque(row) for row in rows])
        return Universe(deque([cells]))

    def part1(self) -> int:
        u = self.puzzle.data
        for _ in range(6):
            u = u.run_cycle()
        return sum(1 for layer in u.cells for row in layer for cell in row if cell == "#")

    def part2(self) -> int:
        mu = Multiverse(cells=deque([self.puzzle.data.cells]))
        for _ in range(6):
            mu = mu.run_cycle()
        return sum(1 for universe in mu.cells for layer in universe for row in layer for cell in row if cell == "#")


if __name__ == '__main__':
    SolverDay17(PuzzleDownloader(day=17, parser=SolverDay17.parser).get_puzzle()).run()
