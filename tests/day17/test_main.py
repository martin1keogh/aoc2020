from typing import List, Callable

from aoc2020.day17.main import SolverDay17
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay17(PuzzleExamplesChecker):
    day: int = 17
    solver: SolverDay17 = SolverDay17
    examples: List[Example] = [
        Example(
            data="""\
                .#.
                ..#
                ###""",
            solution_part1=112,
            solution_part2=848,
        )
    ]
    parser: Callable[[str], List[str]] = lambda x, y: SolverDay17.parser(y)
