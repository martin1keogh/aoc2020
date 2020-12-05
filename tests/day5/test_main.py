from typing import List, Callable

from aoc2020.day5.main import SolverDay5, Seat
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay5(PuzzleExamplesChecker):
    day: int = 4
    solver: SolverDay5 = SolverDay5
    examples: List[Example] = [
        Example(data="BFFFBBFRRR", solution_part1=567),
        Example(data="FFFBBBFRRR", solution_part1=119),
        Example(data="BBFFBBFRLL", solution_part1=820),
    ]
    parser: Callable[[str], List[Seat]] = SolverDay5.parser
