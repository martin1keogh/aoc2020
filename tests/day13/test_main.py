from typing import List, Callable

from aoc2020.day13.main import SolverDay13
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay13(PuzzleExamplesChecker):
    day: int = 12
    solver: SolverDay13 = SolverDay13
    examples: List[Example] = [
        Example(
            data="""\
                939
                7,13,x,x,59,x,31,19""",
            solution_part1=295,
            solution_part2=1068781,
        ),
        Example(
            data="""\
                939
                17,x,13,19""",
            solution_part2=3417,
        ),
        Example(
            data="""\
                939
                67,7,59,61""",
            solution_part2=754018,
        ),
        Example(
            data="""\
                939
                67,x,7,59,61""",
            solution_part2=779210,
        ),
        Example(
            data="""\
                939
                67,7,x,59,61""",
            solution_part2=1261476,
        ),
        Example(
            data="""\
                939
                1789,37,47,1889""",
            solution_part2=1202161486,
        ),
    ]
    parser: Callable[[str], List[str]] = lambda x, y: SolverDay13.parser(y)
