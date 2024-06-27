"""
This module helps to manage different key stores.
"""

from os import PathLike, environ
from pathlib import Path

from .store import Store


class StoreManager:
    DEFAULT_STORAGE_ROOT_PATH = Path.home() / ".config" / "spykes"
    STORAGE_ROOT_PATH_ENV_VAR = "SPYKES_ROOT"

    @classmethod
    def get_default(cls):
        return cls(base_path=Path(environ.get(cls.STORAGE_ROOT_PATH_ENV_VAR, cls.DEFAULT_STORAGE_ROOT_PATH)))

    def __init__(self, *, base_path: Path):
        self._base_path = base_path.resolve()
        self._current_path = self._base_path / "current_store"

    def add_store(
        self,
        *,
        name: str,
        repository_url: PathLike,
        initial_public_key: Path | None = None,
    ):
        store = Store.clone(url=repository_url, path=self._base_path / name)
        if initial_public_key:
            store.initialize(public_key_path=initial_public_key)

    def select_store(self, *, name: str):
        store = next(s for s in self.stores if s.name == name)
        self._current_path.unlink(missing_ok=True)
        self._current_path.symlink_to(store.path)

    def list_stores(self):
        for store in self.stores:
            print(store.name)

    @property
    def current_store(self) -> Store:
        return Store(path=self._current_path)

    @property
    def stores(self) -> list[Store]:
        return list(Store(path=path) for path in self._base_path.iterdir())
