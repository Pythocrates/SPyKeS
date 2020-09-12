''' This tests the Store class.
'''

from pathlib import Path
from unittest import mock

from pytest import fixture

from spykes.store import Store


@fixture(scope='class')
def mock_repo():
    with mock.patch('git.Repo'):
        yield


@fixture(scope='class')
def mock_secret():
    with mock.patch('spykes.store.Secret'):
        yield


@fixture(scope='function')
def mock_run():
    with mock.patch('spykes.store.run'):
        yield


class TestStore:
    def test_name(self, mock_repo):
        repo_path = Path('/my/store/path')
        store = Store(path=repo_path)
        assert store.name == 'path'

    def test_path(self, mock_repo):
        repo_path = Path('/my/store/path')
        store = Store(path=repo_path)
        assert store.path == repo_path

    def test_edit(self, mock_repo, mock_run):
        with mock.patch('spykes.store.Secret') as secret:
            repo_path = Path('/my/store/path')
            store = Store(path=repo_path)
            store.edit()
