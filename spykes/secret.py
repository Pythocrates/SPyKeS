"""
This module provides decryption and encryption functions for a temporary file.
"""

from collections.abc import Iterable, Iterator
from contextlib import contextmanager
from os import urandom
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory
from typing import IO

from gnupg import GPG


class Secret:
    def __init__(self, *, path: Path, user_keys_path: Path):
        self._path = path
        self._user_keys_path = user_keys_path
        self._original = None
        self._latest = None
        self._changed = False

    @property
    def path(self) -> Path:
        return self._path

    @property
    def _user_keys(self) -> Iterable[Path]:
        return self._user_keys_path.glob("*.pubkey")

    def force_encryption(self):
        self._original = None

    @property
    def changed(self) -> bool:
        return self._original != self._latest

    @property
    @contextmanager
    def decrypted(self) -> Iterator[str]:
        self._changed = False
        with NamedTemporaryFile(mode="w+b", suffix=".txt", delete=True) as _cf:
            self._decrypt(target=_cf)
            yield _cf.name
            self._shred(target=_cf)

        if self.changed:
            self._encrypt()

    def _decrypt(self, target: IO[bytes]):
        with open(self._path, "rb") as encrypted_file:
            gpg = GPG(use_agent=True, verbose=True)
            gpg.decrypt_file(encrypted_file, output=target.name)
            self._original = open(target.name).read()

    def _encrypt(self):
        with TemporaryDirectory() as temp_dir:
            gpg = GPG(use_agent=True, gnupghome=temp_dir, verbose=True)
            for key_file in self._user_keys:
                gpg.import_keys(open(key_file).read())
            recipients = [k["uids"][0] for k in gpg.list_keys()]
            gpg.encrypt(
                self._latest,
                recipients=recipients,
                output=self._path,
                always_trust=True,
            )

    def _shred(self, *, target: IO[bytes]):
        self._latest = open(target.name).read()
        length = Path(target.name).stat().st_size
        for _ in range(length):
            target.seek(0)
            target.write(urandom(length))
            target.flush()

    def initialize(self):
        self._encrypt()

    def list_users(self):
        for key_path in self._user_keys:
            print(key_path.stem)
