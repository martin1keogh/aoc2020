import os
from dataclasses import dataclass
from pathlib import Path
from typing import Generic, TypeVar, Callable

import requests

T = TypeVar("T")


@dataclass(frozen=True)
class Puzzle(Generic[T]):
    day: int
    data: T


class PuzzleDownloader(Generic[T]):
    def __init__(self, day: int, parser: Callable[[str], T]):
        self.day = day
        self.parser = parser

    def get_puzzle(self) -> Puzzle[T]:
        parsed = self.parser(self._read_data())
        return Puzzle(day=self.day, data=parsed)

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

    def _read_data(self) -> str:
        if not self._data_path.exists():
            self._cache_data()
        return self._data_path.read_text()
