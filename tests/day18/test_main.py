from typing import List, Callable

from aoc2020.day18.main import SolverDay18
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay18(PuzzleExamplesChecker):
    day: int = 18
    solver: SolverDay18 = SolverDay18
    examples: List[Example] = [
        Example(
            data="2 * 3 + (4 * 5)",
            solution_part1=26,
            solution_part2=46,
        ),
        Example(
            data="5 + (8 * 3 + 9 + 3 * 4 * 3)",
            solution_part1=437,
        ),
        Example(
            data="5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))",
            solution_part1=12240,
        ),
        Example(
            data="((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2",
            solution_part1=13632,
        ),
    ]
    parser: Callable[[str], List[str]] = lambda x, y: SolverDay18.parser(y)
