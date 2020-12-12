from __future__ import annotations

from collections import deque
from typing import Literal, Tuple, Union, List, Deque

from pydantic import BaseModel, validator

from aoc2020.shared.parser_utils import linewise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver
from aoc2020.shared.typing_utils import assert_never


class Coord(Tuple[int, int]):
    @property
    def x(self) -> int:
        return self[0]

    @property
    def y(self) -> int:
        return self[1]

    def __add__(self, other: Coord) -> Coord:
        return Coord((self.x + other.x, self.y + other.y))

    @property
    def manhattan_distance(self) -> int:
        return abs(self.x) + abs(self.y)


class Axis(Tuple[int, int]):
    def __mul__(self, other: int) -> Coord:
        return Coord((self[0] * other, self[1] * other))


class Direction(BaseModel):
    __root__: Literal["N", "E", "S", "W"]

    @staticmethod
    def clockwise(from_: Direction) -> Deque[Direction]:
        dirs = deque(map(Direction.parse_obj, ["N", "E", "S", "W"]))
        dirs.rotate(-dirs.index(from_))  # sneaky minus sign here
        return dirs

    @property
    def axis(self) -> Axis:
        if self.__root__ == "N":
            return Axis((0, 1))
        elif self.__root__ == "W":
            return Axis((-1, 0))
        elif self.__root__ == "S":
            return Axis((0, -1))
        elif self.__root__ == "E":
            return Axis((1, 0))
        else:
            assert_never(self.__root__)


class Instruction(BaseModel):
    action: Union[
        Direction,
        Literal["L", "R", "F"],
    ]
    value: int

    @validator("value")
    def _check_rotation_by_90(cls, value, values) -> int:
        action = values["action"]
        if action in ["L", "R"] and not value % 90 == 0:
            raise ValueError
        return value


class Boat(BaseModel):
    direction: Direction
    coord: Coord

    @staticmethod
    def starting_position() -> Boat:
        return Boat(direction="E", coord=Coord((0, 0)))  # type: ignore


class SolverDay12(Solver):
    puzzle: Puzzle[List[Instruction]]

    @staticmethod
    @linewise_parser
    def parser(line: str) -> Instruction:
        action, value = line[0], line[1:]
        return Instruction(action=action, value=value)  # type: ignore

    def part1(self) -> int:
        boat = Boat.starting_position()
        for instruction in self.puzzle.data:
            if isinstance(instruction.action, Direction):
                shift = instruction.action.axis * instruction.value
                boat.coord += shift
            elif instruction.action == "F":
                shift = boat.direction.axis * instruction.value
                boat.coord += shift
            elif instruction.action == "L":
                rotation_number = (360 - instruction.value) // 90
                new_direction = Direction.clockwise(from_=boat.direction)[rotation_number]
                boat.direction = new_direction
            elif instruction.action == "R":
                rotation_number = instruction.value // 90
                new_direction = Direction.clockwise(from_=boat.direction)[rotation_number]
                boat.direction = new_direction
            else:
                assert_never(instruction)
        return boat.coord.manhattan_distance


if __name__ == '__main__':
    SolverDay12(PuzzleDownloader(day=12, parser=SolverDay12.parser).get_puzzle()).run()
