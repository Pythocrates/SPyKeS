'''
This module provides decryption and encryption functions for a temporary file.
'''

from contextlib import contextmanager
from os import urandom
from tempfile import NamedTemporaryFile

import gnupg


class Secret:
    def __init__(self, encrypted_path, user_keys_path):
        self._encrypted_path = encrypted_path
        self._user_keys_path = user_keys_path
        self._file = None
        self._original = None
        self._latest = ''

    def __fspath__(self):
        return self._file.name

    @property
    def _user_keys(self):
        return self._user_keys_path.glob('*.pubkey')

    @property
    @contextmanager
    def decrypted(self):
        self._decrypt()
        yield self
        self._latest = self.__read()
        self._shred()

        if self._modified:
            self._encrypt()

    def _decrypt(self):
        self._file = NamedTemporaryFile(mode='w+b', suffix='.txt', delete=True)
        with open(self._encrypted_path, 'rb') as encrypted_file:
            gpg = gnupg.GPG(use_agent=True, verbose=True)
            gpg.decrypt_file(encrypted_file, output=self)
            self._original = self.__read()

    def _encrypt(self):  # , user_keys):
        gpg = gnupg.GPG(use_agent=True, gnupghome='.', verbose=True)
        for key_file in self._user_keys:
            gpg.import_keys(open(key_file).read())
        recipients = [k['uids'][0] for k in gpg.list_keys()]
        gpg.encrypt(
            self._latest, recipients=recipients,
            output=self._encrypted_path,
            always_trust=True,
        )

    def _shred(self):
        length = self._file.tell()
        for _ in range(length):
            self._file.seek(0)
            self._file.write(urandom(length))
            self._file.flush()

        self._file.close()
        self._file = None

    def __read(self):
        self._file.seek(0)
        return self._file.read()

    @property
    def _modified(self):
        return self._original != self._latest

    def initialize(self):
        self._encrypt()
