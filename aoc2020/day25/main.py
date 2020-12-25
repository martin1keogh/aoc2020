from itertools import islice
from typing import Tuple, Iterator

from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver

CardPK = int
DoorPK = int


class SolverDay25(Solver):
    puzzle: Puzzle
    _divider = 20201227

    def _transformations(self, subject_number: int) -> Iterator[Tuple[int, int]]:
        """Yields the loop number and the its associated value"""
        value = 1
        loop = 0
        while True:
            value *= subject_number
            value %= self._divider
            yield loop, value
            loop += 1

    @staticmethod
    def parser(input_: str) -> Tuple[CardPK, DoorPK]:
        card, door = input_.splitlines()
        return int(card), int(door)

    def part1(self) -> int:
        card_pk, door_pk = self.puzzle.data
        for loop, value in self._transformations(7):
            if value == card_pk:
                return next(islice(self._transformations(door_pk), loop, loop + 1))[1]
            if value == door_pk:
                return next(islice(self._transformations(card_pk), loop, loop + 1))[1]
        raise ValueError  # should be unreachable


if __name__ == '__main__':
    SolverDay25(PuzzleDownloader(day=25, parser=SolverDay25.parser).get_puzzle()).run()
