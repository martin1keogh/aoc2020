from __future__ import annotations

from typing import List, Type

from aoc2020.day8.instructions import Instruction, instruction_parser, Nop, Jmp
from aoc2020.day8.interpreter import Interpreter, LoopDetected
from aoc2020.shared.models import NoResultFoundException
from aoc2020.shared.parser_utils import linewise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver
from aoc2020.shared.typing_utils import assert_never


class SolverDay8(Solver):
    puzzle: Puzzle[List[Instruction]]

    @staticmethod
    @linewise_parser
    def parser(line: str) -> Instruction:
        return instruction_parser(line)

    def part1(self) -> int:
        interpreter = Interpreter(self.puzzle.data)
        try:
            interpreter.run()
            raise NoResultFoundException
        except LoopDetected as ld:
            return ld.final_accumulator_value

    # change the instruction at `index` to the new type, and returns a new list with this change
    def _mutate_instruction(self, index: int, new_instruction_cls: Type[Instruction]) -> List[Instruction]:
        new_instruction_set = self.puzzle.data.copy()
        new_instruction = {**self.puzzle.data[index].dict(by_alias=True), "code": new_instruction_cls.__name__.lower()}
        new_instruction_set[index] = new_instruction_cls.parse_obj(new_instruction)
        return new_instruction_set

    def part2(self) -> int:
        for index, instruction in enumerate(self.puzzle.data):
            if instruction.code == "acc":
                continue
            elif instruction.code == "jmp":
                new_instruction_set = self._mutate_instruction(index, Nop)
            elif instruction.code == "nop":
                new_instruction_set = self._mutate_instruction(index, Jmp)
            else:
                assert_never(instruction.code)

            interpreter = Interpreter(new_instruction_set)

            try:
                return interpreter.run()
            except LoopDetected:
                pass
        raise NoResultFoundException


if __name__ == '__main__':
    SolverDay8(PuzzleDownloader(day=8, parser=SolverDay8.parser).get_puzzle()).run()
