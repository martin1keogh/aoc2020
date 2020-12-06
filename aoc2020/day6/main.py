from typing import List

from pydantic import BaseModel, Field

from aoc2020.shared.parser_utils import groupwise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


class Answers(BaseModel):
    __root__: str = Field(..., regex="^[a-zA-Z]+$")


class SolverDay6(Solver):
    puzzle: Puzzle[List[List[Answers]]]

    @staticmethod
    @groupwise_parser
    def parser(group: List[str]) -> List[Answers]:
        answers = []
        for answer_per_person in group:
            no_blanks = answer_per_person.replace(" ", "")
            answers.append(Answers(__root__=no_blanks))
        return answers

    def part1(self) -> int:
        count = 0
        for answers_per_group in self.puzzle.data:
            answers_in_group = set()
            for answers_per_person in answers_per_group:
                answers_in_group.update(list(answers_per_person.__root__))
            count += len(answers_in_group)
        return count


if __name__ == '__main__':
    SolverDay6(PuzzleDownloader(day=6, parser=SolverDay6.parser).get_puzzle()).run()
