from typing import List, Callable

from aoc2020.day3.main import SolverDay3, Forest
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay3(PuzzleExamplesChecker):
    day: int = 3
    solver: SolverDay3 = SolverDay3
    examples: List[Example] = [
        Example(
            data="""\
                ..##.......
                #...#...#..
                .#....#..#.
                ..#.#...#.#
                .#...##..#.
                ..#.##.....
                .#.#.#....#
                .#........#
                #.##...#...
                #...##....#
                .#..#...#.#""",
            solution_part1=7,
            solution_part2=336
        )
    ]
    # hack to get around the fact that python sucks ass
    parser: Callable[[str], Forest] = lambda x, y: SolverDay3.parser(y)
