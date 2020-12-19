import re
from textwrap import dedent
from typing import Tuple, List

from lark import Lark, LarkError

from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


class SolverDay19(Solver):
    puzzle: Puzzle

    @staticmethod
    def parser(input_: str) -> Tuple[str, str]:
        rule_str, lines = input_.split("\n\n")
        return rule_str, lines

    def _count_ok(self, rules: List[str]) -> int:
        # add an "r" prefix to rules (lark doesn't like rules starting with a digit)
        named_rules = []
        for rule in rules:
            named_rules.append(re.sub(r"(\d+)", r"r\1", rule))

        parser = Lark("\n".join(named_rules), start="r0")
        ok_count = 0
        for line in self.puzzle.data[1].splitlines():
            try:
                parser.parse(line)
                ok_count += 1
            except LarkError:
                pass
        return ok_count

    def part1(self) -> int:
        return self._count_ok(self.puzzle.data[0].splitlines())

    def part2(self) -> int:
        input_rules = []
        for rule in self.puzzle.data[0].splitlines():
            if not (rule.startswith("8:") or rule.startswith("11:")):
                input_rules.append(rule)

        new_rules_str = """\
            8: 42 | 42 8
            11: 42 31 | 42 11 31"""
        new_rules = dedent(new_rules_str).splitlines()
        rules = input_rules + new_rules

        return self._count_ok(rules)


if __name__ == '__main__':
    SolverDay19(PuzzleDownloader(day=19, parser=SolverDay19.parser).get_puzzle()).run()
