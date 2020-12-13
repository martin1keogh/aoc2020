import math
from functools import reduce
from typing import List, Union, Literal

from pydantic import BaseModel

from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver


class Bus(BaseModel):
    frequency: Union[Literal["x"], int]

    def time_until_next_departure(self, arrival_time: int) -> int:
        if self.frequency == "x":
            return 1
        else:
            return -arrival_time % self.frequency  # appears to work... /shrug


class Notes(BaseModel):  # poor name
    arrival_time: int
    buses: List[Bus]


class SolverDay13(Solver):
    puzzle: Puzzle[Notes]

    @property
    def arrival_time(self) -> int:
        return self.puzzle.data.arrival_time

    @staticmethod
    def parser(input_: str) -> Notes:
        line1, line2 = input_.splitlines()
        buses = map(lambda freq: {"frequency": freq}, line2.split(","))
        return Notes(arrival_time=line1, buses=list(buses))  # type: ignore

    def part1(self) -> int:
        only_known_frequencies = [bus for bus in self.puzzle.data.buses if bus.frequency != "x"]
        bus = min(only_known_frequencies, key=lambda bus: bus.time_until_next_departure(self.arrival_time))
        return bus.frequency * bus.time_until_next_departure(self.arrival_time)  # type: ignore

    def part2(self) -> int:
        constraints = []
        for offset, bus in enumerate(self.puzzle.data.buses):
            if bus.frequency == "x":
                continue
            constraints.append((bus.frequency, -offset))

        # check all the frequencies are coprimes
        assert reduce(math.gcd, map(lambda x: x[0], constraints)) == 1

        # chinese remainder algorithm
        result = 0
        m = math.prod(map(lambda x: x[0], constraints))
        for freq, remainder in constraints:
            b = m // freq
            result += remainder * b * pow(b, -1, freq)

        return result % m


if __name__ == '__main__':
    SolverDay13(PuzzleDownloader(day=13, parser=SolverDay13.parser).get_puzzle()).run()
