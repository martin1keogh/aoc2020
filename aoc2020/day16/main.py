from __future__ import annotations

import re
from collections import defaultdict
from dataclasses import dataclass, field
from functools import lru_cache
from typing import List, Type, Dict, Iterator

from pydantic import BaseModel, validator, Field, create_model, ValidationError

from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


class TicketInfo(BaseModel):
    __root__: List[int]


class Notes(BaseModel):
    constraints: List[Type[BaseModel]]
    own_ticket: TicketInfo
    other_tickets: List[TicketInfo]


class _ConstraintDefinition(BaseModel):
    name: str
    constraints: str = Field(..., regex="^(\\d+)-(\\d+) or (\\d+)-(\\d+)$")

    def _validate_range(self, i: int) -> int:
        if range_boundaries := re.match("^(\\d+)-(\\d+) or (\\d+)-(\\d+)$", self.constraints):
            assert int(range_boundaries.group(1)) <= int(i) <= int(range_boundaries.group(2)) or \
                   int(range_boundaries.group(3)) <= int(i) <= int(range_boundaries.group(4))
            return int(i)
        else:
            raise ValueError

    def get_model(self) -> Type[BaseModel]:
        field_name = "__root__"
        validators = {
            "root_validator": validator(field_name, allow_reuse=True)(self._validate_range)
        }
        return create_model(self.name, __root__=(int, ...), __validators__=validators)


@dataclass
class SolverDay16(Solver):
    puzzle: Puzzle[Notes]
    _invalid_constraint_position: Dict = field(default_factory=lambda: defaultdict(set))

    @staticmethod
    def parser(input_: str) -> Notes:
        constraints_, own, others = map(str.splitlines, input_.split("\n\n"))

        constraints = []
        for c in constraints_:
            name, ranges = c.split(": ")
            model = _ConstraintDefinition(name=name, constraints=ranges)
            constraints.append(model.get_model())

        own_ticket = TicketInfo(__root__=own[-1].split(","))

        other_tickets = []
        for t in others[1:]:
            ticket_info = TicketInfo(__root__=t.split(","))
            other_tickets.append(ticket_info)

        return Notes(
            constraints=constraints,
            own_ticket=own_ticket,
            other_tickets=other_tickets
        )

    def part1(self) -> int:
        invalid_sum = 0
        for o in self.puzzle.data.other_tickets:
            for v in o.__root__:
                for c in self.puzzle.data.constraints:
                    try:
                        c(__root__=v)
                        break
                    except ValidationError:
                        continue
                else:
                    invalid_sum += v

        return invalid_sum

    def __hash__(self) -> int:
        return 1

    @lru_cache(maxsize=None)
    def _valid_constraint_at_position(self, constraint: Type[BaseModel], pos: int) -> bool:
        try:
            for ticket in self.puzzle.data.other_tickets:
                constraint(__root__=ticket.__root__[pos])
        except ValidationError:
            return False
        return True

    def _find_valid_constraint_order(self,
                                     acc: List[Type[BaseModel]],
                                     constraints: List[Type[BaseModel]],
                                     constraint_index: int
                                     ) -> Iterator[List[Type[BaseModel]]]:
        if not constraints:
            yield acc
        else:
            for i in range(len(constraints)):
                copy = constraints.copy()
                c = copy.pop(i)
                if self._valid_constraint_at_position(c, constraint_index):
                    yield from self._find_valid_constraint_order(acc + [c], copy, constraint_index + 1)

    def part2(self) -> int:
        # remove invalid tickets (at least one impossible constraint)
        for o in self.puzzle.data.other_tickets.copy():
            for v in o.__root__:
                for c in self.puzzle.data.constraints:
                    try:
                        c(__root__=v)
                        break
                    except ValidationError:
                        continue
                else:
                    self.puzzle.data.other_tickets.remove(o)

        reordered_constraints = self._find_valid_constraint_order([], self.puzzle.data.constraints, 0)

        result = 1
        for constraint, value in zip(next(reordered_constraints), self.puzzle.data.own_ticket.__root__):
            if constraint.__name__.startswith("departure"):
                result *= value

        return result


if __name__ == '__main__':
    SolverDay16(PuzzleDownloader(day=16, parser=SolverDay16.parser).get_puzzle()).run()
