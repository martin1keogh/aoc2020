from typing import List, Callable

from aoc2020.day12.main import SolverDay12
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay12(PuzzleExamplesChecker):
    day: int = 12
    solver: SolverDay12 = SolverDay12
    examples: List[Example] = [
        Example(
            data="""\
                F10
                N3
                F7
                R90
                F11""",
            solution_part1=25,
            solution_part2=286,
        ),
    ]
    parser: Callable[[str], List[str]] = lambda x, y: SolverDay12.parser(y)
