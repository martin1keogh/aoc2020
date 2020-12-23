from __future__ import annotations

from dataclasses import dataclass
from itertools import islice, chain, dropwhile
from typing import Optional, Reversible, Callable

from aoc2020.shared.puzzle import Puzzle
from aoc2020.shared.solver import Solver


@dataclass(eq=True)
class Node:
    data: int
    next: LL


@dataclass(eq=True)
class LL:
    node: Optional[Node]

    def __repr__(self) -> str:
        if not self.node:
            return "Nil"
        else:
            return f"{self.node.data}::" + repr(self.node.next)

    @staticmethod
    def from_iterable(iterable: Reversible[int]) -> LL:  # bit stringent here, sue me
        result = LL(None)
        for elem in reversed(iterable):
            result.prepend(elem)
        return result

    # doesn't seem to work with the type annotations?
    # @singledispatchmethod
    # def append(self, data) -> LL:
    #     raise NotImplemented
    #
    # @append.register
    # def _(self, data: int) -> LL:
    #     if not self.node:
    #         return LL(Node(data, None))
    #     elif not self.node.next:
    #         return LL(Node(self.node.data, LL(Node(data, None))))
    #
    # @append.register

    def append(self, tail: LL) -> None:
        last: Optional[Node] = None
        for node in self:
            last = node

        if not last:
            self.node = tail.node
        else:
            last.next = tail

    def insert(self, index: int, to_insert: LL) -> None:
        if index < 0:
            raise ValueError

        for node in self:
            if index == 0:
                to_insert.append(node.next)
                node.next = to_insert
                break
            else:
                index -= 1
        else:
            raise ValueError

    def insert_after_match(self, p: Callable[[int], bool], to_insert: LL) -> None:
        for node in self:
            if p(node.data):
                to_insert.append(node.next)
                node.next = to_insert
                break
        else:
            raise ValueError

    def prepend(self, data: int) -> None:
        self.node = Node(data, LL(self.node))

    def __iter__(self):
        node = self.node
        yield node
        while node := node.next.node:
            yield node

    def head(self) -> int:
        return self.node.data

    def tail(self) -> LL:
        return self.node.next

    def pop(self) -> int:
        if not self.node:
            raise IndexError
        data = self.node.data
        self.node = self.node.next.node
        return data


class SolverDay23(Solver):
    puzzle: Puzzle[LL]

    def part1(self) -> int:
        cups = self.puzzle.data
        min_cup = min(map(lambda cup: cup.data, cups))
        max_cup = max(map(lambda cup: cup.data, cups))

        for _ in range(100):
            head = cups.pop()
            removed = []
            for _ in range(3):
                removed.append(cups.pop())

            target = head - 1
            if target < min_cup:
                target = max_cup
            while target in removed:
                target -= 1
                if target < min_cup:
                    target = max_cup

            cups.insert_after_match(lambda x: x == target, LL.from_iterable(removed))
            cups.append(LL(Node(head, LL(None))))

        chained = chain(cups, cups)
        from_1 = dropwhile(lambda x: x.data != 1, chained)
        return int("".join(islice(map(lambda cup: str(cup.data), from_1), 1, 9)))


if __name__ == '__main__':
    SolverDay23(Puzzle(day=23, data=LL.from_iterable(list(map(int, "562893147"))))).run()
