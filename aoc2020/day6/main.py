from functools import reduce
from typing import List

from aoc2020.shared.parser_utils import groupwise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


class SolverDay6(Solver):
    puzzle: Puzzle[List[List[str]]]

    @staticmethod
    @groupwise_parser
    def parser(group: List[str]) -> List[str]:
        answers = []
        for answer_per_person in group:
            no_blanks = answer_per_person.replace(" ", "")
            answers.append(no_blanks)
        return answers

    def part1(self) -> int:
        count = 0
        for answers_per_group in self.puzzle.data:
            answers_in_group = set()
            for answers_per_person in answers_per_group:
                answers_in_group.update(list(answers_per_person))
            count += len(answers_in_group)
        return count

    def part2(self) -> int:
        count = 0
        for answers_per_group in self.puzzle.data:
            as_sets = map(set, answers_per_group)
            common_answers = reduce(set.intersection, as_sets)
            count += len(common_answers)
        return count


if __name__ == '__main__':
    SolverDay6(PuzzleDownloader(day=6, parser=SolverDay6.parser).get_puzzle()).run()
