'''
This module contains key storing capabilities.
'''

from os import environ as env
from shutil import copy2
from subprocess import CalledProcessError, run

import git

from .secret import Secret


class Store:
    EDITOR = next((env[k] for k in ['VISUAL', 'EDITOR'] if k in env), 'vi')

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._repo_path = path.resolve()
        self._repo = git.Repo(self._repo_path)
        self._user_keys_path = self._repo_path / 'user-keys'
        self._secret = Secret(
            self._repo_path / 'keys.asc',
            self._user_keys_path)

    @property
    def name(self):
        return self._repo_path.stem

    @property
    def path(self):
        return self._repo_path

    def _get_remote(self):
        self._repo.remotes.origin.pull()

    def _put_remote(self, users=None, keys=None):
        if users:
            self._repo.index.add([self._user_keys_path.as_posix()])
            self._repo.index.commit(message=users)

        if keys:
            self._repo.index.add([self._secret.path.as_posix()])
            self._repo.index.commit(message=keys)

        if not any([users, keys]):
            self._repo.index.add([
                self._user_keys_path.as_posix(),
                self._secret.path.as_posix(),
            ])
            run(['git', 'commit'], cwd=self._repo_path, check=True)

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
            run(['less', clear_file], check=True)

    @classmethod
    def clone(cls, url, path):
        git.Repo.clone_from(url=url, to_path=path)
        return cls(path=path)

    def initialize(self, public_key_path):
        ''' Initialize an empty store with an empty key file and own pubkey.
        '''
        self._user_keys_path.mkdir(parents=True, exist_ok=True)
        self.add_user(public_key_path, reencrypt=False)
        self._secret.initialize()
        self._put_remote(keys='Add empty key file.')

    def list_users(self):
        self._secret.list_users()

    def add_user(self, public_key, reencrypt=True):
        copy2(public_key, self._user_keys_path)
        self._put_remote(users=f'Add user {public_key.stem}.')
        if reencrypt:
            with self._secret.decrypted:
                self._secret.force_encryption()
