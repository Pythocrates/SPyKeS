#! /usr/bin/env python3

''' SPyKeS - your Simple Python Key Storage.
'''

from argparse import ArgumentParser
from os import environ as env, urandom
from pathlib import Path
from subprocess import CalledProcessError, run
from tempfile import NamedTemporaryFile

import git
import gnupg


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


class DecryptedTemporaryFile:
    def __init__(self, encrypted_path):
        self._encrypted_path = encrypted_path
        self._gpg = gnupg.GPG(use_agent=True)
        self._gpg.encoding = 'utf-8'
        self._file = None
        self._original = None

    def __enter__(self):
        self._decrypt()
        return self

    def __exit__(self, type_, value, traceback):
        self._shred()
        self._file.close()

    def __fspath__(self):
        return self._file.name

    def _decrypt(self):
        self._file = NamedTemporaryFile(mode='w+b', suffix='.txt', delete=True)
        with open(self._encrypted_path, 'rb') as encrypted_file:
            self._gpg.decrypt_file(encrypted_file, output=self)
            self._original = self.latest

    def encrypt(self, recipients):
        self._gpg.encrypt(
            self.latest, recipients=recipients,
            output=self._encrypted_path
        )

    def _shred(self):
        length = self._file.tell()
        for _ in range(length):
            self._file.seek(0)
            self._file.write(urandom(length))
            self._file.flush()

    @property
    def latest(self):
        self._file.seek(0)
        return self._file.read()

    @property
    def modified(self):
        return self._original != self.latest


def _parse_args():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name')

    subparsers.add_parser('edit')
    subparsers.add_parser('show')

    return parser.parse_args()


def main():
    args = _parse_args()
    store = Store(path=Path.home() / 'clones' / 'simple-keystore')
    getattr(store, args.subparser_name)()


if __name__ == '__main__':
    main()
