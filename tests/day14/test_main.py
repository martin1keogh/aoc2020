from typing import List, Callable

from aoc2020.day14.main import SolverDay14
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay14(PuzzleExamplesChecker):
    day: int = 14
    solver: SolverDay14 = SolverDay14
    examples: List[Example] = [
        Example(
            data="""\
                mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
                mem[8] = 11
                mem[7] = 101
                mem[8] = 0""",
            solution_part1=165,
        )
    ]
    parser: Callable[[str], List[str]] = lambda x, y: SolverDay14.parser(y)
