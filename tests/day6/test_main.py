from typing import List, Callable

from aoc2020.day6.main import SolverDay6, Answer
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay6(PuzzleExamplesChecker):
    day: int = 6
    solver: SolverDay6 = SolverDay6
    examples: List[Example] = [
        Example(
            data="""\
                abc

                a
                b
                c

                ab
                ac

                a
                a
                a
                a

                b""",
            solution_part1=11),
    ]
    parser: Callable[[str], List[Answer]] = SolverDay6.parser
