from typing import List

from aoc2020.day15.main import SolverDay15
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay15(PuzzleExamplesChecker):
    day: int = 15
    solver: SolverDay15 = SolverDay15
    examples: List[Example] = [
        Example(
            data=[0, 3, 6],
            solution_part1=436,
        ),
        Example(
            data=[1, 3, 2],
            solution_part1=1,
        ),
        Example(
            data=[2, 1, 3],
            solution_part1=10,
        ),
        Example(
            data=[1, 2, 3],
            solution_part1=27,
        ),
        Example(
            data=[2, 3, 1],
            solution_part1=78,
        ),
        Example(
            data=[3, 2, 1],
            solution_part1=438,
        ),
        Example(
            data=[3, 1, 2],
            solution_part1=1836,
        ),
    ]
