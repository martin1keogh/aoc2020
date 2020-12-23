from __future__ import annotations

from collections import deque
from itertools import islice, chain, dropwhile, tee
from math import prod
from typing import Deque, List

from toolz import partition

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

    def part2(self) -> int:
        nb_round = 10_000_000
        nb_elems = 1_000_000
        cups = self.puzzle.data.copy()

        min_cup = 1
        max_cup = nb_elems
        cups = cups + deque(range(len(cups) + 1, nb_elems + 1))

        # bit random, no real idea on how to guess the best value here?
        nb_groups = 50
        group_size = nb_elems // nb_groups

        # divide into multiple smaller deque to try and avoid some heavy .insert() on the middle of a 1m element deque
        partitioned: List[Deque[int]] = list(map(deque, partition(group_size, cups)))
        cup_to_group = {c: i // group_size for i, c in enumerate(cups)}

        for round_ in range(nb_round):
            # we pop 4 elements from the first deque every time, so we have to
            # refresh the partition every group_size / 4 loop (ignoring the fact that
            # we sometime insert into the first partition)
            if round_ % (group_size // 4) == 0:
                # redistribute everything
                # the data will naturally skew to the last deque, this flattens everything once more
                m1, m2 = tee(chain(*partitioned))
                cup_to_group = {c: i // group_size for i, c in enumerate(m1)}
                partitioned = list(map(deque, partition(group_size, m2)))

            if round_ % 10_000 == 0:
                print(round_)

            current = partitioned[0].popleft()
            removed = [partitioned[0].popleft() for _ in range(3)]

            target = current - 1
            if target < min_cup:
                target = max_cup
            while target in removed:
                target -= 1
                if target < min_cup:
                    target = max_cup

            group = cup_to_group[target]
            i = partitioned[group].index(target)

            for x in reversed(removed):
                cup_to_group[x] = group
                partitioned[group].insert(i + 1, x)

            cup_to_group[current] = nb_groups - 1
            partitioned[-1].append(current)

        cups = list(chain(*partitioned))
        chained = chain(cups, cups)
        from_1 = dropwhile(lambda x: x != 1, chained)
        return prod(islice(from_1, 1, 3))


if __name__ == '__main__':
    SolverDay23(Puzzle(day=23, data=deque(map(int, "562893147")))).run()
