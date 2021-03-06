from typing import List, Callable

from aoc2020.day16.main import SolverDay16
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay16(PuzzleExamplesChecker):
    day: int = 16
    solver: SolverDay16 = SolverDay16
    examples: List[Example] = [
        Example(
            data="""\
                class: 1-3 or 5-7
                row: 6-11 or 33-44
                seat: 13-40 or 45-50

                your ticket:
                7,1,14

                nearby tickets:
                7,3,47
                40,4,50
                55,2,20
                38,6,12""",
            solution_part1=71,
        ),
        Example(
            data="""\
                class: 0-1 or 4-19
                departure_row: 0-5 or 8-19
                departure_seat: 0-13 or 16-19

                your ticket:
                11,12,13

                nearby tickets:
                3,9,18
                15,1,5
                5,14,9""",
            solution_part2=143
        )
    ]
    parser: Callable[[str], List[str]] = lambda x, y: SolverDay16.parser(y)
