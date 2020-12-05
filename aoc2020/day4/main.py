import re
from itertools import groupby
from typing import List, Optional, Union, Literal

from pydantic import BaseModel, ValidationError, Field, MissingError, validator

from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


class Passport(BaseModel):
    ecl: Literal["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]
    pid: str = Field(..., regex="^\\d{9}$")
    eyr: int = Field(..., ge=2020, le=2030)
    hcl: str = Field(..., regex="^#[0-9a-f]{6}$")
    byr: int = Field(..., ge=1920, le=2002)
    iyr: int = Field(..., ge=2010, le=2020)
    hgt: str
    cid: Optional[str]

    @validator("hgt")
    def _height_is_valid(cls, height: str) -> str:
        regex = "^(\\d{2,3})(in|cm)$"
        if match := re.match(regex, height):
            if match.group(2) == "in" and not 59 <= int(match.group(1)) <= 76:
                raise ValueError("Invalid inch value")
            if match.group(2) == "cm" and not 150 <= int(match.group(1)) <= 193:
                raise ValueError("Invalid centimeter value")
            return height  # should be transformed into a class of it's own, but... efforts
        raise ValueError("Invalid height value")


class SolverDay4(Solver):
    puzzle: Puzzle[List[Union[ValidationError, Passport]]]

    @staticmethod
    def parser(lines: str) -> List[Union[ValidationError, Passport]]:
        passports: List[Union[ValidationError, Passport]] = []

        reconstructed_lines = []
        line_groups = groupby(lines.splitlines(), lambda line: len(line) == 0)
        for is_empty, group in line_groups:
            if not is_empty:
                reconstructed_lines.append(" ".join(group))

        for line in reconstructed_lines:
            fields_as_str = line.split(" ")
            as_dict = dict(map(lambda s: s.split(":"), fields_as_str))  # type: ignore
            try:
                passports.append(Passport.parse_obj(as_dict))
            except ValidationError as v:
                passports.append(v)
        return passports

    def part1(self) -> int:
        count = 0
        for maybe_passport in self.puzzle.data:
            if isinstance(maybe_passport, Passport):
                count += 1
            # part 1 doesn't care about anything but the correct fields being there (ie the MissingError)
            elif all(map(lambda err: not isinstance(err.exc, MissingError), maybe_passport.raw_errors)):  # type: ignore
                count += 1
        return count

    def part2(self) -> int:
        count = 0
        for maybe_passport in self.puzzle.data:
            if isinstance(maybe_passport, Passport):
                count += 1
        return count


if __name__ == '__main__':
    SolverDay4(PuzzleDownloader(day=4, parser=SolverDay4.parser).get_puzzle()).run()
