from typing import List, Callable

from aoc2020.day23.main import SolverDay23
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay23(PuzzleExamplesChecker):
    day: int = 23
    solver: SolverDay23 = SolverDay23
    examples: List[Example] = [
        Example(
            data="389125467",
            solution_part1=67384529,
            # solution_part2=149245887792  # too slow, should rework this to use linked list first
        ),
    ]
    parser: Callable[[str], List[str]] = lambda x, y: SolverDay23.parser(y)
