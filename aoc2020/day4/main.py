from itertools import groupby
from typing import List, Optional, Union

from pydantic import BaseModel, ValidationError

from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


class Passport(BaseModel):
    ecl: str
    pid: str
    eyr: str
    hcl: str
    byr: str
    iyr: str
    hgt: str
    cid: Optional[str]


class SolverDay4(Solver):
    puzzle: Puzzle[List[Passport]]

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
            as_dict = dict(map(lambda s: s.split(":"), fields_as_str))
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
        return count


if __name__ == '__main__':
    SolverDay4(PuzzleDownloader(day=4, parser=SolverDay4.parser).get_puzzle()).run()
