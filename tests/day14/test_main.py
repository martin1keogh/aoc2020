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
        ),
        Example(
            data="""\
                mask = 000000000000000000000000000000X1001X
                mem[42] = 100
                mask = 00000000000000000000000000000000X0XX
                mem[26] = 1""",
            solution_part2=208,
        )
    ]
    parser: Callable[[str], List[str]] = lambda x, y: SolverDay14.parser(y)
