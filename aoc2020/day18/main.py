# type: ignore

from __future__ import annotations

import re
from shlex import shlex
from typing import List, Iterator

from aoc2020.shared.parser_utils import linewise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


def evaluate(input_: Iterator[str]) -> int:
    res = None
    op = None
    for sym in input_:
        if sym == "(":
            res2 = evaluate(input_)
            if not res:
                res = res2
            else:
                if op == "+":
                    res += int(res2)
                elif op == "*":
                    res *= int(res2)
                else:
                    raise ValueError
        elif sym == ")":
            return res
        elif sym.isdigit():
            if not res:
                res = int(sym)
            elif not op:
                raise ValueError
            else:
                if op == "+":
                    res += int(sym)
                elif op == "*":
                    res *= int(sym)
                else:
                    raise ValueError
        else:
            op = sym
    return res


class C:
    def __init__(self, value: int):
        self.value = value

    def __add__(self, other: C) -> C:
        return C(self.value * other.value)

    def __mul__(self, other: C) -> C:
        return C(self.value + other.value)


def eval_advanced(input_: Iterator[str]) -> int:
    s = "".join(input_)
    s = s.translate(str.maketrans("+*", "*+"))
    s = re.sub("(\\d+)", "C(\\1)", s)
    # lol
    return eval(s).value


class SolverDay18(Solver):
    puzzle: Puzzle[List[str]]

    @staticmethod
    @linewise_parser
    def parser(line: str) -> str:
        return line

    def part1(self) -> int:
        input_ = map(lambda s: iter(shlex(s)), self.puzzle.data)
        return sum(map(evaluate, input_))

    def part2(self) -> int:
        return sum(map(eval_advanced, self.puzzle.data))


if __name__ == '__main__':
    SolverDay18(PuzzleDownloader(day=18, parser=SolverDay18.parser).get_puzzle()).run()
