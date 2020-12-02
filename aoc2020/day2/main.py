from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Tuple, NewType, Any, Dict, Literal, Type

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


class ValidatedPassword(BaseModel, ABC):
    policy: CorporatePolicy
    password: Password

    @classmethod
    @abstractmethod
    def _valid_password(cls, password: str, policy: CorporatePolicy) -> Literal[True]:
        """Actual password validation. Returns true if OK, raises a validation error otherwise"""
        ...

    @validator("password")
    def _check_password_is_valid(cls, password: str, values: Dict[str, Any]) -> str:
        if policy := values.get("policy"):
            if isinstance(policy, CorporatePolicy) and cls._valid_password(password, policy):
                return password
            else:
                raise TypeError
        raise ValueError


class ValidatedPasswordOldCompany(ValidatedPassword):
    @classmethod
    def _valid_password(cls, password: str, policy: CorporatePolicy) -> Literal[True]:
        count = password.count(policy.required_char)
        if policy.min_rep <= count <= policy.max_rep:
            return True
        else:
            raise ValueError(f"Wrong number of {policy.required_char} in {password}."
                             f" Got {count}, expected between {policy.min_rep} and {policy.max_rep}")


class ValidatedPasswordNewCompany(ValidatedPassword):
    @classmethod
    def _valid_password(cls, password: str, policy: CorporatePolicy) -> Literal[True]:
        # no specs on out of bound values
        count = [password[policy.min_rep - 1], password[policy.max_rep - 1]].count(policy.required_char)
        if count == 1:
            return True
        elif count == 0:
            raise ValueError(f"No {policy.required_char} at indices {policy.min_rep}/{policy.max_rep}.")
        else:
            raise ValueError(f"Both characters {policy.min_rep} and {policy.max_rep} are {policy.required_char}")


@dataclass
class SolverDay2(Solver):
    puzzle: Puzzle[Tuple[CorporatePolicy, Password]]

    @classmethod
    def parser(cls, string: str) -> Tuple[CorporatePolicy, Password]:
        policy, password = string.split(": ")
        return CorporatePolicy.from_str(policy), Password(password)

    def _solve_for(self, validation: Type[ValidatedPassword]) -> int:
        count = 0
        for policy, password in self.puzzle.data:
            try:
                validation(policy=policy, password=password)
                count += 1
            except ValidationError:
                pass
        return count

    def part1(self) -> int:
        return self._solve_for(ValidatedPasswordOldCompany)

    def part2(self) -> int:
        return self._solve_for(ValidatedPasswordNewCompany)


if __name__ == '__main__':
    SolverDay2(PuzzleDownloader(day=2, row_parser=SolverDay2.parser).get_puzzle()).run()
