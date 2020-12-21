from __future__ import annotations

from collections import defaultdict
from functools import reduce
from itertools import permutations
from typing import List, Tuple, NewType, Dict, Set

from aoc2020.shared.models import NoResultFoundException
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

    def _find_ingredients_with_allergens(self) -> Set[Ingredient]:
        allergen_to_food: Dict[Allergen, List[Set[Ingredient]]] = defaultdict(list)
        for ingredients, allergens in self.puzzle.data:
            for allergen in allergens:
                allergen_to_food[allergen].append(ingredients)

        allergen_to_possible_ingredients: Dict[Allergen, Set[Ingredient]] = {}
        for allergen, possible_ingredients in allergen_to_food.items():
            allergen_to_possible_ingredients[allergen] = reduce(set.intersection, possible_ingredients)  # type: ignore

        with_allergens = set(ing for ing_list in allergen_to_possible_ingredients.values() for ing in ing_list)
        return with_allergens

    def part1(self) -> int:
        with_allergens = self._find_ingredients_with_allergens()
        return sum(len(ingredients - with_allergens) for ingredients, _ in self.puzzle.data)

    def part2(self) -> str:  # type: ignore
        known_allergens = list(set(allergen for _, allergens in self.puzzle.data for allergen in allergens))
        allergenic_ingredients = list(self._find_ingredients_with_allergens())

        # brute force, try all allergens combinations (with a 1-to-1 mapping to ingredients)
        for arrangement in permutations(known_allergens):
            allergen_to_ingredient = []
            for i, allergen in enumerate(arrangement):
                allergen_to_ingredient.append((allergen, allergenic_ingredients[i]))

            for all_ingredients, allergens in self.puzzle.data:
                ingredients = all_ingredients & set(allergenic_ingredients)
                expected_ingredients = set(ing for aller, ing in allergen_to_ingredient if aller in allergens)
                if not set(expected_ingredients) <= ingredients:
                    break
            else:
                allergen_to_ingredient.sort(key=lambda t: t[0])
                return ",".join(map(lambda t: t[1], allergen_to_ingredient))
        else:
            raise NoResultFoundException


if __name__ == '__main__':
    SolverDay21(PuzzleDownloader(day=21, parser=SolverDay21.parser).get_puzzle()).run()
