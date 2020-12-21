from __future__ import annotations

from collections import defaultdict
from functools import reduce
from typing import List, Tuple, NewType, Dict, Set

from aoc2020.shared.parser_utils import linewise_parser
from aoc2020.shared.puzzle import Puzzle, PuzzleDownloader
from aoc2020.shared.solver import Solver

Ingredient = NewType("Ingredient", str)
Allergen = NewType("Allergen", str)


class SolverDay21(Solver):
    puzzle: Puzzle[List[Tuple[Set[Ingredient], Set[Allergen]]]]

    @staticmethod
    @linewise_parser
    def parser(line: str) -> Tuple[Set[Ingredient], Set[Allergen]]:
        ingredients_str, allergens_str = line.split("(")
        ingredients = ingredients_str.split()
        allergens_str = allergens_str[1:-1]  # remove parentheses
        allergens_str = allergens_str[8:]  # remove "contains"
        allergens = allergens_str.split(", ")
        return set(map(Ingredient, ingredients)), set(map(Allergen, allergens))

    def part1(self) -> int:
        allergen_to_possible_ingredients: Dict[Allergen, List[Set[Ingredient]]] = defaultdict(list)
        for ingredients, allergens in self.puzzle.data:
            for allergen in allergens:
                allergen_to_possible_ingredients[allergen].append(ingredients)

        for allergen, possible_ingredients in allergen_to_possible_ingredients.items():
            allergen_to_possible_ingredients[allergen] = reduce(set.intersection, possible_ingredients)  # type: ignore

        with_allergens = set(ing for ing_list in allergen_to_possible_ingredients.values() for ing in ing_list)
        ok_count = 0
        for ingredients, _ in self.puzzle.data:
            ok_count += len(ingredients - with_allergens)
        return ok_count


if __name__ == '__main__':
    SolverDay21(PuzzleDownloader(day=21, parser=SolverDay21.parser).get_puzzle()).run()
