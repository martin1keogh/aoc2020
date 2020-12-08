from __future__ import annotations

import re
from typing import List, Literal, ClassVar, Set

from pydantic import BaseModel

from aoc2020.shared.parser_utils import linewise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver
from aoc2020.shared.typing_utils import assert_never


class Instruction(BaseModel):
    code: Literal["acc", "nop", "jmp"]
    arg1: int

    regex: ClassVar[str] = "(?P<code>\\w{3}) (?P<arg1>(\+|-)\\d+)"


class SolverDay8(Solver):
    puzzle: Puzzle[List[Instruction]]

    @staticmethod
    @linewise_parser
    def parser(line: str) -> Instruction:
        if match := re.match(Instruction.regex, line):
            return Instruction.parse_obj(match.groupdict())
        else:
            raise ValueError(f"Unknown instruction {line}")

    def part1(self) -> int:
        accumulator = 0
        current_index = 0
        visited_indices: Set[int] = set()
        while current_index not in visited_indices:
            visited_indices.add(current_index)
            current_instruction = self.puzzle.data[current_index]
            if current_instruction.code == "acc":
                accumulator += current_instruction.arg1
                current_index += 1
            elif current_instruction.code == "nop":
                current_index += 1
            elif current_instruction.code == "jmp":
                current_index += current_instruction.arg1
            else:
                assert_never(current_instruction.code)
        return accumulator


if __name__ == '__main__':
    Instruction.update_forward_refs()
    SolverDay8(PuzzleDownloader(day=8, parser=SolverDay8.parser).get_puzzle()).run()
