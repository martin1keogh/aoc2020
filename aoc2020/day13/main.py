import math
from dataclasses import dataclass
from functools import reduce
from typing import List, Tuple

from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


@dataclass
class Notes:
    arrival_time: int
    buses: List[Tuple[int, int]]


class SolverDay13(Solver):
    puzzle: Puzzle[Notes]

    @staticmethod
    def parser(input_: str) -> Notes:
        line1, line2 = input_.splitlines()
        buses = [(i, int(bus)) for i, bus in enumerate(line2.split(",")) if bus != "x"]
        return Notes(arrival_time=int(line1), buses=buses)

    def part1(self) -> int:
        with_times_to_wait = [(bus, -self.puzzle.data.arrival_time % bus) for _, bus in self.puzzle.data.buses]
        bus, ttw = min(with_times_to_wait, key=lambda wttw: wttw[1])
        return bus * ttw

    def part2(self) -> int:
        # check all the frequencies are coprimes
        assert reduce(math.gcd, (freq for _, freq in self.puzzle.data.buses)) == 1

        # chinese remainder algorithm
        result = 0
        m = math.prod(freq for _, freq in self.puzzle.data.buses)

        for remainder, freq in self.puzzle.data.buses:
            b = m // freq
            result += - remainder * b * pow(b, -1, freq)

        return result % m


if __name__ == '__main__':
    SolverDay13(PuzzleDownloader(day=13, parser=SolverDay13.parser).get_puzzle()).run()
