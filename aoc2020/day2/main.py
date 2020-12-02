from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Tuple, NewType, Any, Dict

from pydantic import BaseModel, validator, ValidationError, Field
from pydantic.types import PositiveInt

from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


class CorporatePolicy(BaseModel):
    min_rep: PositiveInt
    max_rep: PositiveInt
    required_char: str = Field(..., regex=r"^[a-z]$")

    _regex_from_str: re.Pattern = re.compile("""(?P<min_rep>\\d+)-(?P<max_rep>\\d+) (?P<required_char>[a-z])""")

    @staticmethod
    def from_str(string: str) -> CorporatePolicy:
        if matches := CorporatePolicy._regex_from_str.match(string):
            return CorporatePolicy(**matches.groupdict())
        raise ValueError


Password = NewType("Password", str)


class ValidatedPassword(BaseModel):
    policy: CorporatePolicy
    password: Password

    @validator("password")
    def _check_password_is_valid(cls, password: str, values: Dict[str, Any]) -> str:
        if policy := values.get("policy"):
            if isinstance(policy, CorporatePolicy):
                count = password.count(policy.required_char)
                if policy.min_rep <= count <= policy.max_rep:
                    return password
                else:
                    raise ValueError(f"Wrong number of {policy.required_char} in {password}."
                                     f" Got {count}, expected between {policy.min_rep} and {policy.max_rep}")
            else:
                raise TypeError
        raise ValueError



@dataclass
class SolverDay2(Solver):
    puzzle: Puzzle[Tuple[CorporatePolicy, Password]]

    @classmethod
    def parser(cls, string: str) -> Tuple[CorporatePolicy, Password]:
        policy, password = string.split(":")
        return CorporatePolicy.from_str(policy), Password(password)

    def part1(self) -> int:
        count = 0
        for policy, password in self.puzzle.data:
            try:
                ValidatedPassword(policy=policy, password=password)
                count += 1
            except ValidationError:
                pass
        return count


if __name__ == '__main__':
    SolverDay2(PuzzleDownloader(day=2, row_parser=SolverDay2.parser).get_puzzle()).run()
