'''
This module contains key storing capabilities.
'''

from os import environ as env
from subprocess import CalledProcessError, run

import git

from spykes.decrypted_temporary_file import DecryptedTemporaryFile


class Store:
    EDITOR = next((env[k] for k in ['VISUAL', 'EDITOR'] if k in env), 'vi')

    def __init__(self, path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._repo_path = path
        self._repo = git.Repo(self._repo_path)
        self._keys_path = self._repo_path / 'keys.asc'
        self._recipients_path = self._repo_path / 'encrypt-to-users'

    @property
    def recipients(self):
        return [r.strip() for r in open(self._recipients_path).readlines()]

    def edit(self):
        self._repo.remotes.origin.pull()

        with DecryptedTemporaryFile(self._keys_path) as dtf:
            try:
                run([self.EDITOR, dtf], check=True)
            except CalledProcessError:
                pass  # TODO: Log something?
            else:
                if dtf.modified:
                    dtf.encrypt(recipients=self.recipients)
                    self._repo.index.add([self._keys_path.as_posix()])
                    # TODO: commit & push

    def show(self):
        self._repo.remotes.origin.pull()
        with DecryptedTemporaryFile(self._keys_path) as dtf:
            run(['less', dtf], check=True)
