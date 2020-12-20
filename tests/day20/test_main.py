from typing import List, Callable

from aoc2020.day20.main import SolverDay20
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay20(PuzzleExamplesChecker):
    day: int = 20
    solver: SolverDay20 = SolverDay20
    examples: List[Example] = [
        Example(
            data="""\
                Tile 2311:
                ..##.#..#.
                ##..#.....
                #...##..#.
                ####.#...#
                ##.##.###.
                ##...#.###
                .#.#.#..##
                ..#....#..
                ###...#.#.
                ..###..###

                Tile 1951:
                #.##...##.
                #.####...#
                .....#..##
                #...######
                .##.#....#
                .###.#####
                ###.##.##.
                .###....#.
                ..#.#..#.#
                #...##.#..

                Tile 1171:
                ####...##.
                #..##.#..#
                ##.#..#.#.
                .###.####.
                ..###.####
                .##....##.
                .#...####.
                #.##.####.
                ####..#...
                .....##...

                Tile 1427:
                ###.##.#..
                .#..#.##..
                .#.##.#..#
                #.#.#.##.#
                ....#...##
                ...##..##.
                ...#.#####
                .#.####.#.
                ..#..###.#
                ..##.#..#.

                Tile 1489:
                ##.#.#....
                ..##...#..
                .##..##...
                ..#...#...
                #####...#.
                #..#.#.#.#
                ...#.#.#..
                ##.#...##.
                ..##.##.##
                ###.##.#..

                Tile 2473:
                #....####.
                #..#.##...
                #.##..#...
                ######.#.#
                .#...#.#.#
                .#########
                .###.#..#.
                ########.#
                ##...##.#.
                ..###.#.#.

                Tile 2971:
                ..#.#....#
                #...###...
                #.#.###...
                ##.##..#..
                .#####..##
                .#..####.#
                #..#.#..#.
                ..####.###
                ..#.#.###.
                ...#.#.#.#

                Tile 2729:
                ...#.#.#.#
                ####.#....
                ..#.#.....
                ....#..#.#
                .##..##.#.
                .#.####...
                ####.#.#..
                ##.####...
                ##..#.##..
                #.##...##.

                Tile 3079:
                #.#.#####.
                .#..######
                ..#.......
                ######....
                ####.#..#.
                .#...#.##.
                #.#####.##
                ..#.###...
                ..#.......
                ..#.###...""",
            solution_part1=20899048083289,
        ),
        Example(
            data="""\
                tile 1:
                #.#
                #.#
                ...
                
                tile 2:
                #.#
                #.#
                ...
                
                tile 3:
                #.#
                #.#
                ...
                
                tile 4:
                #.#
                #.#
                ...
            """,
            solution_part1=24,
        ),
        Example(
            data="""\
                tile 1:
                ##.
                ...
                ...
                
                tile 2:
                ###
                ###
                .##
                
                tile 3:
                ...
                ...
                ...
                
                tile 4:
                .##
                ...
                ...
            """,
            solution_part1=24,
        ),
    ]
    parser: Callable[[str], List[str]] = lambda x, y: SolverDay20.parser(y)
