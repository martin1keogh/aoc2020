from dataclasses import dataclass
from typing import ClassVar

from aoc2020.shared.puzzle import Puzzle
from aoc2020.shared.solver import Solver


@dataclass
class SolverDay1(Solver):
    puzzle: Puzzle[int] = Puzzle(day=1, row_parser=int)

    TARGET: ClassVar = 2020

    def part1(self) -> int:
        sorted_input = sorted(self.puzzle.input)
        for i, v1 in enumerate(sorted_input):
            for v2 in sorted_input[i + i:]:
                s = v1 + v2
                if s == self.TARGET:
                    return v1 * v2
                if s > self.TARGET:
                    break
        else:
            raise ValueError  # find a better exception

    def part2(self) -> int:
        sorted_input = sorted(self.puzzle.input)
        for i, v1 in enumerate(sorted_input):
            for j, v2 in enumerate(sorted_input[i + 1:]):
                s1 = v1 + v2
                if s1 > self.TARGET:
                    break

                for v3 in sorted_input[i + j + i:]:
                    s2 = s1 + v3
                    if s2 == self.TARGET:
                        return v1 * v2 * v3
                    if s2 > self.TARGET:
                        break
        else:
            raise ValueError  # find a better exception


if __name__ == '__main__':
    SolverDay1().run()
