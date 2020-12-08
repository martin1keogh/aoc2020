from dataclasses import field, dataclass
from typing import List, Set

from aoc2020.day8.instructions import Instruction, Acc, Nop, Jmp
from aoc2020.shared.typing_utils import assert_never


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

        if isinstance(current_instruction, Acc):
            self._accumulator += current_instruction.value
            self._current_index += 1
        elif isinstance(current_instruction, Nop):
            self._current_index += 1
        elif isinstance(current_instruction, Jmp):
            self._current_index += current_instruction.offset
        else:
            assert_never(current_instruction.code)
