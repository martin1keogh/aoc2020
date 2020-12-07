from __future__ import annotations

import re
from dataclasses import field, InitVar
from functools import lru_cache
from typing import List, Dict, ClassVar

import pydantic
from pydantic import validator

from aoc2020.shared.parser_utils import linewise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver

Bag = str


# can't seem to find a way to do `init=False` with BaseModel instead
@pydantic.dataclasses.dataclass
class BagColorCodeSpecifier:
    __root__: InitVar[str]
    container: Bag = field(init=False)
    containees: Dict[Bag, int] = field(init=False)

    _container_regex = "(\\w+ \\w+) bags"
    _containee_regex = "(\\d+) (\\w+ \\w+) bags?"

    def __post_init__(self, __root__: str) -> None:
        self.container, self.containees = __root__.split(" contain ")

    @validator("container", pre=True)
    def _validate_container(cls, container: str) -> Bag:
        if match := re.match(cls._container_regex, container):
            return match.group(1)
        raise ValueError

    @validator("containees", pre=True)
    def _validate_containees(cls, containees: str) -> Dict[Bag, int]:
        if containees == "no other bags.":
            return dict()

        result = dict()
        for bag_str in containees.split(", "):
            if match := re.match(cls._containee_regex, bag_str):
                result[match.group(2)] = int(match.group(1))
            else:
                raise ValueError

        return result


class SolverDay7(Solver):
    puzzle: Puzzle[List[BagColorCodeSpecifier]]
    _can_hold_target_cache: Dict[Bag, bool]

    TARGET: ClassVar[Bag] = "shiny gold"

    @staticmethod
    @linewise_parser
    def parser(line: str) -> BagColorCodeSpecifier:
        return BagColorCodeSpecifier(line)

    @property
    def specifications(self) -> Dict[Bag, Dict[Bag, int]]:
        return {spec.container: spec.containees for spec in self.puzzle.data}

    # needed for lru_cache to work, unused otherwise
    def __hash__(self):
        return 0

    @lru_cache(maxsize=None)
    def _can_hold_target(self, bag: Bag) -> bool:
        # hopefully there's no cycle
        specs = self.specifications[bag].keys()
        return self.TARGET in specs or any(self._can_hold_target(nested_bag) for nested_bag in specs)

    def part1(self) -> int:
        count = 0
        for spec in self.puzzle.data:
            if self._can_hold_target(spec.container):
                count += 1
        return count

    @lru_cache(maxsize=None)
    def _number_of_bag_inside(self, bag: Bag) -> int:
        specs = self.specifications[bag]
        total_count = 1
        for nested_bag, count in specs.items():
            total_count += count * self._number_of_bag_inside(nested_bag)
        return total_count

    def part2(self) -> int:
        return self._number_of_bag_inside(self.TARGET) - 1  # do not count the TARGET itsef


if __name__ == '__main__':
    SolverDay7(PuzzleDownloader(day=7, parser=SolverDay7.parser).get_puzzle()).run()
