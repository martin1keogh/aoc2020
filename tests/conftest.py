from tests.utils.puzzle_examples_checker import PuzzleExamplesChecker


def pytest_generate_tests(metafunc):
    if issubclass(metafunc.cls, PuzzleExamplesChecker):
        if metafunc.definition.name == "test_part1":
            filter_ = lambda example: example.solution_part1
        elif metafunc.definition.name == "test_part2":
            filter_ = lambda example: example.solution_part2
        else:
            raise ValueError

        metafunc.parametrize("example", filter(filter_, metafunc.cls.examples))
