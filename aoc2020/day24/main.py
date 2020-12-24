from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import List, Tuple, Set, Iterator

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


Coord = Tuple[int, int]


# same as day 17, mostly
@dataclass
class TileSet:
    black_tiles: Set[Coord]
    dimensions: Coord  # ~= max coordinates

    def __contains__(self, item: Coord) -> bool:
        for dim_item, dim_self in zip(item, self.dimensions):
            if not abs(dim_item) <= dim_self:
                return False
        return True

    def _neighbors(self, x: int, y: int) -> Iterator[Coord]:
        return [
            (x+1, y),
            (x-1, y),
            (x+1, y-1),
            (x, y-1),
            (x, y+1),
            (x-1, y+1),
        ]

    def expand(self) -> TileSet:
        return TileSet(
            black_tiles=self.black_tiles.copy(),
            dimensions=(self.dimensions[0] + 1, self.dimensions[1] + 1)
        )

    def run_cycle(self) -> TileSet:
        new_tileset = self.expand()
        (x, y) = new_tileset.dimensions

        for xx in range(-x, x+1):
            for yy in range(-y, y+1):
                active_neighbors = len(set(new_tileset._neighbors(xx, yy)) & self.black_tiles)
                tile_is_black = (xx, yy) in self.black_tiles
                if not tile_is_black and active_neighbors == 2:
                    new_tileset.black_tiles.add((xx, yy))
                elif tile_is_black and (active_neighbors == 0 or active_neighbors > 2):
                    new_tileset.black_tiles.remove((xx, yy))

        return new_tileset


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
            to_append = tuple(map(sum, (zip(*map(lambda direction: direction.axis, path)))))
            to_flip.append(to_append)

        count = 0
        for tile, flips in groupby(identity, to_flip).items():
            if len(flips) % 2 == 1:
                count += 1

        return count

    def part2(self) -> int:
        to_flip = []
        for path in self.puzzle.data:
            to_append = tuple(map(sum, (zip(*map(lambda direction: direction.axis, path)))))
            to_flip.append(to_append)

        black_tiles = set()
        for tile, flips in groupby(identity, to_flip).items():
            if len(flips) % 2 == 1:
                black_tiles.add(tile)

        ts = TileSet(black_tiles=black_tiles, dimensions=(100, 100))  # Big enough
        for _ in range(100):
            ts = ts.run_cycle()

        return len(ts.black_tiles)


if __name__ == '__main__':
    SolverDay24(PuzzleDownloader(day=24, parser=SolverDay24.parser).get_puzzle()).run()
