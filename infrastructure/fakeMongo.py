from typing import Any
from copy import deepcopy


class FakeCollection():

    @property
    def file(self) -> dict[int, Any]:
        return self._files

    def __init__(self) -> None:
        self._files: dict[int, Any] = {}
        self._current_idx = 0

    def create(self, file: Any) -> Any:

        while self._current_idx in self._files:
            self._current_idx += 1

        file.id = self._current_idx
        self._files[file.id] = deepcopy(file)
        self._current_idx += 1
        return file

    def read(self, id: int) -> Any | None:

        if (id in self._files):
            return self._files[id]

        return None

    def update(self, id: int, file: Any) -> Any:

        if (id not in self._files):
            raise KeyError(f"Id: {id} cannot be found in database")

        self._files[id] = deepcopy(file)
        return file

    def delete(self, id: int) -> None:
        if (id in self._files):
            del self._files[id]

    def list_all(self) -> list[Any]:
        all_file = [deepcopy(self._files[idx]) for idx in self._files]
        return all_file


class FakeMongo():

    def __init__(self) -> None:
        self._collections: dict[str, FakeCollection] = {}

    def get_collection(self, col_name: str) -> FakeCollection:

        if col_name not in self._collections:
            self._collections[col_name] = FakeCollection()
        return self._collections[col_name]

    def del_collection(self, col_name: str):
        if col_name in self._collections:
            del self._collections[col_name]
