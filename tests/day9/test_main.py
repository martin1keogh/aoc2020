from typing import List, Callable

from aoc2020.day9.main import SolverDay9
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay9(PuzzleExamplesChecker):
    def solver_(self, puzzle):
        return SolverDay9(puzzle, pool_size=5)

    day: int = 9
    solver: SolverDay9 = solver_
    examples: List[Example] = [
        Example(
            data="""\
                35
                20
                15
                25
                47
                40
                62
                55
                65
                95
                102
                117
                150
                182
                127
                219
                299
                277
                309
                576""",
            solution_part1=127,
            solution_part2=62,
        ),
    ]
    parser: Callable[[str], List[str]] = SolverDay9.parser
