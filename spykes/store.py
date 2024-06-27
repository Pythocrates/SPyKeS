"""
This module contains key storing capabilities.
"""

from os import PathLike, environ
from pathlib import Path
from shutil import copy2
from subprocess import CalledProcessError, run
from typing import Self

import git

from .secret import Secret


class Store:
    EDITOR = next((environ[k] for k in ["VISUAL", "EDITOR"] if k in environ), "vi")

    def __init__(self, *, path: Path):
        self._repo_path = path.resolve()
        self._repo = git.Repo(self._repo_path)
        self._user_keys_path = self._repo_path / "user-keys"
        self._secret = Secret(path=self._repo_path / "keys.asc", user_keys_path=self._user_keys_path)

    @property
    def name(self) -> str:
        return self._repo_path.stem

    @property
    def path(self) -> Path:
        return self._repo_path

    def _get_remote(self):
        self._repo.remotes.origin.pull()

    def _put_remote(self, *, user_message: str | None = None, key_message: str | None = None):
        if user_message:
            self._repo.index.add([self._user_keys_path.as_posix()])
            self._repo.index.commit(message=user_message)

        if key_message:
            self._repo.index.add([self._secret.path.as_posix()])
            self._repo.index.commit(message=key_message)

        if not any([user_message, key_message]):
            self._repo.index.add(
                [
                    self._user_keys_path.as_posix(),
                    self._secret.path.as_posix(),
                ]
            )
            run(["git", "commit"], cwd=self._repo_path, check=True)

        self._repo.remotes.origin.push()

    def edit(self):
        self._get_remote()

        with self._secret.decrypted as clear_file:
            try:
                run([self.EDITOR, clear_file], check=True)
            except CalledProcessError:
                return  # TODO: Log something?

        if self._secret.changed:
            self._put_remote()

    def show(self):
        self._get_remote()
        with self._secret.decrypted as clear_file:
            run([self.EDITOR, clear_file], check=True)

    @classmethod
    def clone(cls, *, url: PathLike, path: Path) -> Self:
        git.Repo.clone_from(url=url, to_path=path)
        return cls(path=path)

    def initialize(self, *, public_key_path: Path):
        """Initialize an empty store with an empty key file and own pubkey."""
        self._user_keys_path.mkdir(parents=True, exist_ok=True)
        self.add_user(public_key=public_key_path, reencrypt=False)
        self._secret.initialize()
        self._put_remote(key_message="Add empty key file.")

    def list_users(self):
        self._secret.list_users()

    def add_user(self, *, public_key: Path, reencrypt: bool = True):
        copy2(public_key, self._user_keys_path)
        self._put_remote(user_message=f"Add user {public_key.stem}.")
        if reencrypt:
            with self._secret.decrypted:
                self._secret.force_encryption()
