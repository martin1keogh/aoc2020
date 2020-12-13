from typing import List, Callable

from aoc2020.day13.main import SolverDay13
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay13(PuzzleExamplesChecker):
    day: int = 12
    solver: SolverDay13 = SolverDay13
    examples: List[Example] = [
        Example(
            data="""\
                939
                7,13,x,x,59,x,31,19""",
            solution_part1=295,
        ),
    ]
    parser: Callable[[str], List[str]] = lambda x, y: SolverDay13.parser(y)
