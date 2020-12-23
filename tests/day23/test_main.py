from typing import List

from aoc2020.day23.main import SolverDay23, LL
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay23(PuzzleExamplesChecker):
    day: int = 23
    solver: SolverDay23 = SolverDay23
    examples: List[Example] = [
        Example(
            data=LL.from_iterable(list(map(int, "389125467"))),
            solution_part1=67384529,
            # solution_part2=149245887792
        ),
    ]
