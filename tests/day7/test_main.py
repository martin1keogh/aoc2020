from typing import List, Callable

from aoc2020.day7.main import SolverDay7
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay6(PuzzleExamplesChecker):
    day: int = 7
    solver: SolverDay7 = SolverDay7
    examples: List[Example] = [
        Example(
            data="""\
                light red bags contain 1 bright white bag, 2 muted yellow bags.
                dark orange bags contain 3 bright white bags, 4 muted yellow bags.
                bright white bags contain 1 shiny gold bag.
                muted yellow bags contain 2 shiny gold bags, 9 faded blue bags.
                shiny gold bags contain 1 dark olive bag, 2 vibrant plum bags.
                dark olive bags contain 3 faded blue bags, 4 dotted black bags.
                vibrant plum bags contain 5 faded blue bags, 6 dotted black bags.
                faded blue bags contain no other bags.
                dotted black bags contain no other bags.""",
            solution_part1=4,
            solution_part2=32,
        ),
    ]
    parser: Callable[[str], List[str]] = SolverDay7.parser
