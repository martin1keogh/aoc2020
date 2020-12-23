from __future__ import annotations

from collections import deque
from itertools import islice, chain, dropwhile
from typing import Deque

from aoc2020.shared.puzzle import Puzzle
from aoc2020.shared.solver import Solver


class SolverDay23(Solver):
    puzzle: Puzzle[Deque[int]]

    @staticmethod
    def parser(input_: str) -> Deque[int]:
        return deque(map(int, list(input_)))

    def part1(self) -> int:
        cups = self.puzzle.data.copy()
        min_cup = min(cups)
        max_cup = max(cups)

        for _ in range(100):
            current = cups.popleft()
            removed = [cups.popleft() for _ in range(3)]

            target = current - 1
            if target < min_cup:
                target = max_cup
            while target in removed:
                target -= 1
                if target < min_cup:
                    target = max_cup

            i = cups.index(target)
            for x in reversed(removed):
                cups.insert(i + 1, x)
            cups.append(current)

        chained = chain(cups, cups)
        from_1 = dropwhile(lambda x: x != 1, chained)
        return int("".join(islice(map(str, from_1), 1, len(cups))))


if __name__ == '__main__':
    SolverDay23(Puzzle(day=23, data=deque(map(int, "562893147")))).run()
