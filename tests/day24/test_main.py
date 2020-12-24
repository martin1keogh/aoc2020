from typing import List, Callable

from aoc2020.day24.main import SolverDay24
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay24(PuzzleExamplesChecker):
    day: int = 24
    solver: SolverDay24 = SolverDay24
    examples: List[Example] = [
        Example(
            data="""\
                sesenwnenenewseeswwswswwnenewsewsw
                neeenesenwnwwswnenewnwwsewnenwseswesw
                seswneswswsenwwnwse
                nwnwneseeswswnenewneswwnewseswneseene
                swweswneswnenwsewnwneneseenw
                eesenwseswswnenwswnwnwsewwnwsene
                sewnenenenesenwsewnenwwwse
                wenwwweseeeweswwwnwwe
                wsweesenenewnwwnwsenewsenwwsesesenwne
                neeswseenwwswnwswswnw
                nenwswwsewswnenenewsenwsenwnesesenew
                enewnwewneswsewnwswenweswnenwsenwsw
                sweneswneswneneenwnewenewwneswswnese
                swwesenesewenwneswnwwneseswwne
                enesenwswwswneneswsenwnewswseenwsese
                wnwnesenesenenwwnenwsewesewsesesew
                nenewswnwewswnenesenwnesewesw
                eneswnwswnwsenenwnwnwwseeswneewsenese
                neswnwewnwnwseenwseesewsenwsweewe
                wseweeenwnesenwwwswnew""",
            solution_part1=10,
        ),
    ]
    parser: Callable[[str], List[str]] = lambda x, y: SolverDay24.parser(y)
