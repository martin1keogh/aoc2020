from __future__ import annotations

from collections import deque
from itertools import islice
from typing import Tuple, Deque, Iterable

from aoc2020.shared.parser_utils import groupwise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver

Deck = Deque[int]


class SolverDay22(Solver):
    puzzle: Puzzle[Tuple[Deck, Deck]]

    @staticmethod
    @groupwise_parser
    def parser(group: Iterable[str]) -> Deck:
        return deque(map(int, list(group)[1:]))

    @staticmethod
    def _count_score(deck: Deck) -> int:
        score = 0
        for i, card in enumerate(reversed(deck)):
            score += (i + 1) * card
        return score

    @staticmethod
    def _combat(d1: Deck, d2: Deck) -> int:
        try:
            while True:
                c1, c2 = d1.popleft(), d2.popleft()
                if c1 > c2:
                    d1.extend([c1, c2])
                elif c1 < c2:
                    d2.extend([c2, c1])
                else:
                    raise ValueError
        except IndexError:
            if not d1:
                winning_deck = d2
            elif not d2:
                winning_deck = d1
            else:
                raise ValueError
        return SolverDay22._count_score(winning_deck)

    def part1(self) -> int:
        d1, d2 = self.puzzle.data
        d1, d2 = d1.copy(), d2.copy()
        return SolverDay22._combat(d1, d2)

    @staticmethod
    def _recursive_combat(d1: Deck, d2: Deck) -> Tuple[int, bool]:
        seen = set()
        while True:
            if not d1:
                return SolverDay22._count_score(d2), False
            if not d2:
                return SolverDay22._count_score(d1), True

            as_tuple = (tuple(d1), tuple(d2))
            if as_tuple in seen:
                return SolverDay22._count_score(d1), True
            seen.add(as_tuple)

            c1, c2 = d1.popleft(), d2.popleft()
            if len(d1) < c1 or len(d2) < c2:
                p1_winner = c1 > c2
            else:
                _, p1_winner = SolverDay22._recursive_combat(deque(islice(d1, 0, c1)), deque(islice(d2, 0, c2)))

            if p1_winner:
                d1.extend([c1, c2])
            else:
                d2.extend([c2, c1])

    def part2(self) -> int:
        d1, d2 = self.puzzle.data
        return SolverDay22._recursive_combat(d1, d2)[0]


if __name__ == '__main__':
    SolverDay22(PuzzleDownloader(day=22, parser=SolverDay22.parser).get_puzzle()).run()
