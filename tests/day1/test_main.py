from typing import List

from aoc2020.day1.main import SolverDay1
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay1(PuzzleExamplesChecker):
    day: int = 1
    solver: SolverDay1 = SolverDay1
    examples: List[Example] = [
        Example(
            data=[1721, 979, 366, 299, 675, 1456],
            solution_part1=514579,
            solution_part2=241861950
        )
    ]
