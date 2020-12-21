from typing import List, Callable

from aoc2020.day21.main import SolverDay21
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay21(PuzzleExamplesChecker):
    day: int = 21
    solver: SolverDay21 = SolverDay21
    examples: List[Example] = [
        Example(
            data="""\
                mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
                trh fvjkl sbzzf mxmxvkd (contains dairy)
                sqjhc fvjkl (contains soy)
                sqjhc mxmxvkd sbzzf (contains fish)""",
            solution_part1=5,
        ),
    ]
    parser: Callable[[str], List[str]] = lambda x, y: SolverDay21.parser(y)
