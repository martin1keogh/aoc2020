import os
from pathlib import Path
from typing import Generic, TypeVar, Callable
from typing import List

import requests

T = TypeVar("T")


class Puzzle(Generic[T]):
    def __init__(self, day: int, row_parser: Callable[[str], T]):
        self.day = day
        self.input: List[T] = []
        for line in self._read_data():
            self.input.append(row_parser(line))

    def _download_data(self) -> str:
        url = f"https://adventofcode.com/2020/day/{self.day}/input"
        session = os.environ["AOC_SESSION"]
        headers = {"cookie": f"session={session}"}
        response = requests.get(url=url, headers=headers)
        return response.text

    @property
    def _data_path(self) -> Path:
        return Path(f"ressources/day_{self.day}/input")

    def _cache_data(self) -> None:
        file = self._data_path
        file.parent.mkdir(parents=True, exist_ok=True)
        file.write_text(self._download_data())

    def _read_data(self) -> List[str]:
        if not self._data_path.exists():
            self._cache_data()
        return self._data_path.read_text().splitlines()
