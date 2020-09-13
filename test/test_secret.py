''' This tests the Secret class.
'''

from pathlib import Path
from unittest import mock

from pytest import fixture

from spykes.secret import Secret


@fixture(scope='class')
def mock_gpg():
    with mock.patch('gnupg.GPG'):
        yield


class TestSecret:
    @staticmethod
    def test_path():
        path_1 = Path('/my/path')
        path_2 = Path('/my/path/2')
        secret = Secret(path=path_1, user_keys_path=path_2)
        assert secret.path == path_1

    @staticmethod
    def test_list_keys(capsys):
        path_1 = Path('/my/path')
        path_2 = Path('test/data')
        secret = Secret(path=path_1, user_keys_path=path_2)
        secret.list_users()
        captured = capsys.readouterr()
        assert captured.out in {
            "test_1\ntest_2\n",
            "test_2\ntest_1\n",
        }

    @staticmethod
    def test_initialize(mock_gpg):
        path_1 = Path('test/data/test_encrypted')
        path_2 = Path('test/data')
        secret = Secret(path=path_1, user_keys_path=path_2)

        secret.initialize()

    @staticmethod
    def test_context_manager_changed(mock_gpg):
        path_1 = Path('test/data/test_encrypted')
        path_2 = Path('test/data')
        secret = Secret(path=path_1, user_keys_path=path_2)

        with secret.decrypted as decrypted_path:
            with open(decrypted_path, 'w') as decrypted_file:
                decrypted_file.write('test')

        assert secret.changed

    @staticmethod
    def test_context_manager_unchanged(mock_gpg):
        path_1 = Path('test/data/test_encrypted')
        path_2 = Path('test/data')
        secret = Secret(path=path_1, user_keys_path=path_2)

        with secret.decrypted as decrypted_path:
            with open(decrypted_path, 'w'):
                pass

        assert not secret.changed

        secret.force_encryption()
        assert secret.changed
