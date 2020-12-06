from typing import List

from pydantic import BaseModel, Field

from aoc2020.shared.parser_utils import groupwise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


class Answer(BaseModel):
    __root__: str = Field(..., regex="^[a-zA-Z]$")

    def __hash__(self) -> int:
        return self.__root__.__hash__()


class SolverDay6(Solver):
    puzzle: Puzzle[List[List[Answer]]]

    @staticmethod
    @groupwise_parser
    def parser(line: str) -> List[Answer]:
        no_blanks = line.replace(" ", "")
        return list(map(lambda char: Answer(__root__=char), list(no_blanks)))

    def part1(self) -> int:
        count = 0
        for answer_group in self.puzzle.data:
            distinct_answers_in_group = set(answer_group)
            count += len(distinct_answers_in_group)
        return count


if __name__ == '__main__':
    SolverDay6(PuzzleDownloader(day=6, parser=SolverDay6.parser).get_puzzle()).run()
