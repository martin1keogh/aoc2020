from typing import List, Callable

from aoc2020.day10.main import SolverDay10
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay10(PuzzleExamplesChecker):
    day: int = 10
    solver: SolverDay10 = SolverDay10
    examples: List[Example] = [
        Example(
            data="""\
                16
                10
                15
                5
                1
                11
                7
                19
                6
                12
                4""",
            solution_part1=35,
            solution_part2=8,
        ),
        Example(
            data="""\
                28
                33
                18
                42
                31
                14
                46
                20
                48
                47
                24
                23
                49
                45
                19
                38
                39
                11
                1
                32
                25
                35
                8
                17
                7
                9
                4
                2
                34
                10
                3""",
            solution_part1=220,
            solution_part2=19208,
        ),
    ]
    parser: Callable[[str], List[str]] = SolverDay10.parser
