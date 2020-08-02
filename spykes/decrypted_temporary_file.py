'''
This module provides decryption and encryption functions for a temporary file.
'''

from os import urandom
from tempfile import NamedTemporaryFile

import gnupg


class DecryptedTemporaryFile:
    def __init__(self, encrypted_path):
        self._encrypted_path = encrypted_path
        self._in_gpg = gnupg.GPG(use_agent=True, verbose=True)
        self._out_gpg = gnupg.GPG(use_agent=True, gnupghome='.', verbose=True)
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
            self._in_gpg.decrypt_file(encrypted_file, output=self)
            self._original = self._latest

    def encrypt(self, user_keys):
        for key_file in user_keys:
            self._out_gpg.import_keys(open(key_file).read())
        recipients = [k['uids'][0] for k in self._out_gpg.list_keys()]
        self._out_gpg.encrypt(
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

    @property
    def _latest(self):
        self._file.seek(0)
        return self._file.read()

    @property
    def modified(self):
        return self._original != self._latest

    def initialize(self, user_keys):
        self._file = NamedTemporaryFile(mode='w+b', suffix='.txt', delete=True)
        self.encrypt(user_keys=user_keys)
        self._file.close()
        self._file = None
