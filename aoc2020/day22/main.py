from __future__ import annotations

from collections import deque
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

    def part1(self) -> int:
        d1, d2 = self.puzzle.data
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


if __name__ == '__main__':
    SolverDay22(PuzzleDownloader(day=22, parser=SolverDay22.parser).get_puzzle()).run()
