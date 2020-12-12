from __future__ import annotations

from collections import deque
from typing import Literal, Union, List, Deque, Dict

from pydantic import BaseModel, validator

from aoc2020.shared.parser_utils import linewise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver
from aoc2020.shared.typing_utils import assert_never


class Coord(BaseModel):
    x: int
    y: int

    def __add__(self, vector: Vector) -> Coord:
        return Coord(x=self.x + vector.x, y=self.y + vector.y)

    @property
    def manhattan_distance(self) -> int:
        return abs(self.x) + abs(self.y)


class Vector(Coord):
    def __mul__(self, other: int) -> Vector:
        return Vector(x=self.x * other, y=self.y * other)

    def __add__(self, vector: Vector) -> Vector:
        return Vector(x=self.x + vector.x, y=self.y + vector.y)

    def rotate_clockwise(self) -> Vector:
        return Vector(x=self.y, y=-self.x)


class Direction(BaseModel):
    __root__: Literal["N", "E", "S", "W"]

    @staticmethod
    def clockwise(from_: Direction) -> Deque[Direction]:
        dirs = deque(map(Direction.parse_obj, ["N", "E", "S", "W"]))
        dirs.rotate(-dirs.index(from_))  # sneaky minus sign here
        return dirs

    @property
    def axis(self) -> Vector:
        if self.__root__ == "N":
            return Vector(x=0, y=1)
        elif self.__root__ == "W":
            return Vector(x=-1, y=0)
        elif self.__root__ == "S":
            return Vector(x=0, y=-1)
        elif self.__root__ == "E":
            return Vector(x=1, y=0)
        else:
            assert_never(self.__root__)


class Instruction(BaseModel):
    action: Union[
        Direction,
        Literal["L", "R", "F"],
    ]
    value: int

    @validator("value")
    def _check_rotation_by_90(cls, value: int, values: Dict) -> int:
        action = values["action"]
        if action in ["L", "R"] and not value % 90 == 0:
            raise ValueError
        return value


class Boat(BaseModel):
    direction: Direction
    coord: Coord
    waypoint_offset: Vector

    @staticmethod
    def starting_position() -> Boat:
        return Boat(direction="E", coord=Coord(x=0, y=0), waypoint_offset=Vector(x=10, y=1))  # type: ignore


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
            # `action in ["L", "R"]` makes mypy fail to see we can never reach the `assert_never` (mypy 0.790)
            elif instruction.action == "L" or instruction.action == "R":
                rotation_number = instruction.value // 90
                if instruction.action == "L":
                    rotation_number *= -1
                boat.direction = Direction.clockwise(from_=boat.direction)[rotation_number]
            else:
                assert_never(instruction)
        return boat.coord.manhattan_distance

    def part2(self) -> int:
        boat = Boat.starting_position()
        for instruction in self.puzzle.data:
            if isinstance(instruction.action, Direction):
                shift = instruction.action.axis * instruction.value
                boat.waypoint_offset += shift
            elif instruction.action == "F":
                shift = boat.waypoint_offset * instruction.value
                boat.coord += shift
            elif instruction.action == "L" or instruction.action == "R":
                rotation_number = instruction.value // 90
                if instruction.action == "L":
                    rotation_number *= 3
                for _ in range(rotation_number):
                    boat.waypoint_offset = boat.waypoint_offset.rotate_clockwise()
            else:
                assert_never(instruction)
        return boat.coord.manhattan_distance


if __name__ == '__main__':
    SolverDay12(PuzzleDownloader(day=12, parser=SolverDay12.parser).get_puzzle()).run()
