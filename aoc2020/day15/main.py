from itertools import islice
from typing import List, Dict, Iterator

from aoc2020.shared.puzzle import Puzzle
from aoc2020.shared.solver import Solver


class SolverDay15(Solver):
    puzzle: Puzzle[List[int]]

    def _gen(self) -> Iterator[int]:
        yield from self.puzzle.data

        number_to_last_turn_spoken: Dict[int, int] = {n: i + 1 for i, n in enumerate(self.puzzle.data)}
        last_number = self.puzzle.data[-1]
        turn = len(self.puzzle.data)

        while True:
            if last_number in number_to_last_turn_spoken.keys():
                diff = turn - number_to_last_turn_spoken[last_number]
                number_to_last_turn_spoken[last_number] = turn
                last_number = diff
            else:
                number_to_last_turn_spoken[last_number] = turn
                last_number = 0
            turn += 1
            yield last_number

    def part1(self) -> int:
        for i in islice(self._gen(), 0, 10):
            print(i)
        for i in islice(self._gen(), 2019, 2020):
            return i


if __name__ == '__main__':
    SolverDay15(Puzzle(day=15, data="11,18,0,20,1,7,16".split(","))).run()
