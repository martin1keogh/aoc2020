from typing import List, Callable

from aoc2020.day22.main import SolverDay22
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay22(PuzzleExamplesChecker):
    day: int = 22
    solver: SolverDay22 = SolverDay22
    examples: List[Example] = [
        Example(
            data="""\
                Player 1:
                9
                2
                6
                3
                1

                Player 2:
                5
                8
                4
                7
                10""",
            solution_part1=306,
        ),
    ]
    parser: Callable[[str], List[str]] = lambda x, y: SolverDay22.parser(y)
