from typing import List, Callable

from aoc2020.day25.main import SolverDay25
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay25(PuzzleExamplesChecker):
    day: int = 25
    solver: SolverDay25 = SolverDay25
    examples: List[Example] = [
        Example(
            data="""\
                5764801
                17807724""",
            solution_part1=14897079,
        ),
    ]
    parser: Callable[[str], List[str]] = lambda x, y: SolverDay25.parser(y)
