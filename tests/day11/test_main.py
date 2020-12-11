from typing import List, Callable

from aoc2020.day11.main import SolverDay11
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay11(PuzzleExamplesChecker):
    day: int = 11
    solver: SolverDay11 = SolverDay11
    examples: List[Example] = [
        Example(
            data="""\
                L.LL.LL.LL
                LLLLLLL.LL
                L.L.L..L..
                LLLL.LL.LL
                L.LL.LL.LL
                L.LLLLL.LL
                ..L.L.....
                LLLLLLLLLL
                L.LLLLLL.L
                L.LLLLL.LL""",
            solution_part1=37,
        ),
    ]
    parser: Callable[[str], List[str]] = lambda x, y: SolverDay11.parser(y)
