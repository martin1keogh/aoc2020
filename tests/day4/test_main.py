from typing import List, Callable

from aoc2020.day4.main import SolverDay4, Passport
from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker, Example


class TestSolverDay4(PuzzleExamplesChecker):
    day: int = 4
    solver: SolverDay4 = SolverDay4
    examples: List[Example] = [
        Example(
            data="""\
                ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
                byr:1937 iyr:2017 cid:147 hgt:183cm

                iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
                hcl:#cfa07d byr:1929

                hcl:#ae17e1 iyr:2013
                eyr:2024
                ecl:brn pid:760753108 byr:1931
                hgt:179cm

                hcl:#cfa07d eyr:2025 pid:166559648
                iyr:2011 ecl:brn hgt:59in""",
            solution_part1=2,
        )
    ]
    # hack to get around the fact that python sucks ass
    parser: Callable[[str], List[Passport]] = lambda x, y: SolverDay4.parser(y)
