from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import List, Literal, ClassVar, Set

from pydantic import BaseModel

from aoc2020.shared.models import NoResultFoundException
from aoc2020.shared.parser_utils import linewise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver
from aoc2020.shared.typing_utils import assert_never


class Instruction(BaseModel):
    code: Literal["acc", "nop", "jmp"]
    arg1: int

    regex: ClassVar[str] = "(?P<code>\\w{3}) (?P<arg1>(\\+|-)\\d+)"


class LoopDetected(RuntimeError):
    def __init__(self, acc: int):
        self.final_accumulator_value = acc


@dataclass
class Interpreter:
    instructions: List[Instruction]
    _accumulator: int = field(init=False, default=0)
    _current_index: int = field(init=False, default=0)
    _visited_indices: Set[int] = field(init=False, default_factory=set)

    def run(self) -> int:
        while True:
            if self._current_index in self._visited_indices:
                raise LoopDetected(self._accumulator)
            if self._current_index >= len(self.instructions):
                return self._accumulator
            self.run_step()

    def run_step(self) -> None:
        self._visited_indices.add(self._current_index)
        current_instruction = self.instructions[self._current_index]
        if current_instruction.code == "acc":
            self._accumulator += current_instruction.arg1
            self._current_index += 1
        elif current_instruction.code == "nop":
            self._current_index += 1
        elif current_instruction.code == "jmp":
            self._current_index += current_instruction.arg1
        else:
            assert_never(current_instruction.code)


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
        interpreter = Interpreter(self.puzzle.data)
        try:
            interpreter.run()
            raise NoResultFoundException
        except LoopDetected as ld:
            return ld.final_accumulator_value

    def part2(self) -> int:
        for index, instruction in enumerate(self.puzzle.data):
            if instruction.code == "acc":
                continue
            elif instruction.code == "jmp":
                new_instruction_set = self.puzzle.data.copy()
                new_instruction_set[index] = new_instruction_set[index].copy()
                new_instruction_set[index].code = "nop"
            elif instruction.code == "nop":
                new_instruction_set = self.puzzle.data.copy()
                new_instruction_set[index] = new_instruction_set[index].copy()
                new_instruction_set[index].code = "jmp"
            else:
                assert_never(instruction.code)

            interpreter = Interpreter(new_instruction_set)

            try:
                return interpreter.run()
            except LoopDetected:
                pass
        raise NoResultFoundException


if __name__ == '__main__':
    Instruction.update_forward_refs()
    SolverDay8(PuzzleDownloader(day=8, parser=SolverDay8.parser).get_puzzle()).run()
