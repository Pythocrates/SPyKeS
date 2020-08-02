'''
This module helps to manage different key stores.
'''

from spykes.store import Store


class StoreManager:
    def __init__(self, base_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._base_path = base_path.resolve()
        self._current_path = self._base_path / 'current_store'

    def add_store(self, name, url, initial_key=None):
        store = Store.clone(url=url, path=self._base_path / name)
        if initial_key:
            store.initialize(public_key_path=initial_key)

    def select_store(self, name):
        store = next(s for s in self.stores if s.name == name)
        self._current_path.unlink(missing_ok=True)
        self._current_path.symlink_to(store.path)

    def list_stores(self):
        for store in self.stores:
            print(store.name)

    @property
    def current_store(self):
        return Store(path=self._current_path)

    @property
    def stores(self):
        return list(Store(path=path) for path in self._base_path.iterdir())
