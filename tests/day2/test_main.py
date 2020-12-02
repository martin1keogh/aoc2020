from typing import List, Callable, Tuple

from aoc2020.day2.main import SolverDay2, Password, CorporatePolicy
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay2(PuzzleExamplesChecker):
    day: int = 2
    solver: SolverDay2 = SolverDay2
    examples: List[Example] = [
        Example(
            data="""\
                1-3 a: abcde
                1-3 b: cdefg
                2-9 c: ccccccccc""".splitlines(),
            solution_part1=2,
        )
    ]
    parser: Callable[[str], Tuple[CorporatePolicy, Password]] = SolverDay2.parser
