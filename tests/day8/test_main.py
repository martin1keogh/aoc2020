from typing import List, Callable

from aoc2020.day8.main import SolverDay8
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay6(PuzzleExamplesChecker):
    day: int = 8
    solver: SolverDay8 = SolverDay8
    examples: List[Example] = [
        Example(
            data="""\
                nop +0
                acc +1
                jmp +4
                acc +3
                jmp -3
                acc -99
                acc +1
                jmp -4
                acc +6""",
            solution_part1=5,
            solution_part2=8,
        ),
    ]
    parser: Callable[[str], List[str]] = SolverDay8.parser
