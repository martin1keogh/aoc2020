from __future__ import annotations

import re
from typing import List, Union, Dict, Iterator

from pydantic import Field, BaseModel

from aoc2020.shared.parser_utils import linewise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver
from aoc2020.shared.typing_utils import assert_never


class Mask(BaseModel):
    str_repr: str = Field(..., regex="^(X|0|1){36}$", alias="mask")

    def apply_to(self, bitstring: str) -> str:
        res = list(bitstring.rjust(36, "0"))
        for i, v in enumerate(self.str_repr):
            if v == "X":
                continue
            else:
                res[i] = v
        return "".join(res)

    def apply_to_addr(self, bitstring: str) -> Mask:
        res = list(bitstring.rjust(36, "0"))
        for i, v in enumerate(self.str_repr):
            if v == "0":
                continue
            else:
                res[i] = v
        return Mask(mask="".join(res))

    def generate_all_values(self) -> Iterator[Mask]:  # what a terrible, terrible name
        try:
            i = self.str_repr.index("X")
            s = list(self.str_repr)
            for v in ["0", "1"]:
                s[i] = v
                m = Mask(mask="".join(s))
                yield from m.generate_all_values()
        except ValueError as e:
            yield self


class MemSet(BaseModel):
    address: int = Field(..., ge=0)
    value: int

    def address_as_bitstring(self) -> str:
        return f"{self.address:b}"

    def value_as_bitstring(self) -> str:
        return f"{self.value:b}"


Instruction = Union[Mask, MemSet]


class SolverDay14(Solver):
    puzzle: Puzzle[List[Instruction]]

    class _Builder(BaseModel):
        __root__: Instruction

    @staticmethod
    @linewise_parser
    def parser(line: str) -> Instruction:
        regex = "^(mask = (?P<mask>.*)|mem\\[(?P<address>\\d+)\\] = (?P<value>\\d+))"
        if match := re.match(regex, line):
            return SolverDay14._Builder.parse_obj(match.groupdict()).__root__
        else:
            raise ValueError

    def part1(self) -> int:
        mask = None
        result: Dict[int, int] = {}
        for instruction in self.puzzle.data:
            if isinstance(instruction, Mask):
                mask = instruction
            elif isinstance(instruction, MemSet):
                bitstring = instruction.value_as_bitstring()
                if mask:
                    bitstring = mask.apply_to(bitstring)
                result[instruction.address] = int(bitstring, 2)
            else:
                assert_never(instruction)

        return sum(result.values())

    def part2(self) -> int:
        mask = None
        result: Dict[int, int] = {}
        for instruction in self.puzzle.data:
            if isinstance(instruction, Mask):
                mask = instruction
            elif isinstance(instruction, MemSet):
                if not mask:
                    result[instruction.address] = instruction.value
                else:
                    masked_addr = mask.apply_to_addr(instruction.address_as_bitstring())
                    for sub_mask in masked_addr.generate_all_values():
                        addr = int(sub_mask.str_repr, 2)
                        result[addr] = instruction.value
            else:
                assert_never(instruction)

        return sum(result.values())


if __name__ == '__main__':
    SolverDay14(PuzzleDownloader(day=14, parser=SolverDay14.parser).get_puzzle()).run()
