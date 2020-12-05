from typing import List, Reversible

from pydantic import BaseModel, Field

from aoc2020.shared.parser_utils import linewise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


class Seat(BaseModel):
    specifier: str = Field(..., regex="^(F|B){7}(L|R){3}")

    @staticmethod
    def _to_decimal(bools: Reversible[bool]) -> int:
        """Convert list of 0/1 to its decimal value. Most significant bit first"""
        result = 0
        for power, b in enumerate(reversed(bools)):
            result += b << power
        return result

    @property
    def row(self) -> int:
        row_specifier = self.specifier[:7]
        as_binary_string = map(lambda char: char == "B", list(row_specifier))
        return Seat._to_decimal(list(as_binary_string))

    @property
    def column(self) -> int:
        row_specifier = self.specifier[7:]
        as_binary_string = map(lambda char: char == "R", list(row_specifier))
        return Seat._to_decimal(list(as_binary_string))

    @property
    def id(self) -> int:
        return self.row * 8 + self.column


class SolverDay5(Solver):
    puzzle: Puzzle[List[Seat]]

    @staticmethod
    @linewise_parser
    def parser(line: str) -> Seat:
        return Seat(specifier=line)

    def part1(self) -> int:
        return max(map(lambda seat: seat.id, self.puzzle.data))


if __name__ == '__main__':
    SolverDay5(PuzzleDownloader(day=5, parser=SolverDay5.parser).get_puzzle()).run()
