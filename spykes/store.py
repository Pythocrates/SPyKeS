'''
This module contains key storing capabilities.
'''

from os import environ as env
from shutil import copy2
from subprocess import CalledProcessError, run

import git

from .decrypted_temporary_file import DecryptedTemporaryFile


class Store:
    EDITOR = next((env[k] for k in ['VISUAL', 'EDITOR'] if k in env), 'vi')

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._repo_path = path.resolve()
        self._repo = git.Repo(self._repo_path)
        self._secrects_path = self._repo_path / 'keys.asc'
        self._user_keys_path = self._repo_path / 'user-keys'

    @property
    def name(self):
        return self._repo_path.stem

    @property
    def path(self):
        return self._repo_path

    @property
    def user_keys(self):
        return self._user_keys_path.glob('*.pubkey')

    def _get_remote(self):
        self._repo.remotes.origin.pull()

    def _put_remote(self, users=None, keys=None):
        if users:
            self._repo.index.add([self._user_keys_path.as_posix()])
            self._repo.index.commit(message=users)

        if keys:
            self._repo.index.add([self._secrects_path.as_posix()])
            self._repo.index.commit(message=keys)

        if not any([users, keys]):
            self._repo.index.add([
                self._user_keys_path.as_posix(),
                self._secrects_path.as_posix(),
            ])
            run(['git', 'commit'], cwd=self._repo_path)

        self._repo.remotes.origin.push()

    def edit(self):
        self._get_remote()

        with DecryptedTemporaryFile(self._secrects_path) as dtf:
            try:
                run([self.EDITOR, dtf], check=True)
            except CalledProcessError:
                pass  # TODO: Log something?
            else:
                if dtf.modified:
                    dtf.encrypt(user_keys=self.user_keys)
                    self._put_remote()

    def show(self):
        self._get_remote()
        with DecryptedTemporaryFile(self._secrects_path) as dtf:
            run(['less', dtf], check=True)

    @classmethod
    def clone(cls, url, path):
        git.Repo.clone_from(url=url, to_path=path)
        return cls(path=path)

    def initialize(self, public_key_path):
        ''' Initialize an empty store with an empty key file and own pubkey.
        '''
        self._user_keys_path.mkdir(parents=True, exist_ok=True)
        copy2(public_key_path, self._user_keys_path)
        DecryptedTemporaryFile(self._secrects_path).initialize(
            user_keys=self.user_keys)
        self._put_remote(users=f'Add user {public_key_path.stem}.')
        self._put_remote(keys='Add empty key file.')
