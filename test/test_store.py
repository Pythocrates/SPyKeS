"""
This tests the Store class.
"""

from pathlib import Path
from unittest import mock

from pytest import fixture

from spykes.store import Store


@fixture(scope="class")
def mock_repo():
    with mock.patch("git.Repo"):
        yield


@fixture(scope="class")
def mock_secret():
    with mock.patch("spykes.store.Secret"):
        yield


@fixture(scope="function")
def mock_run():
    with mock.patch("spykes.store.run"):
        yield


REPO_PATH = Path("/my/store/path")


class TestStore:
    def test_name(self, mock_repo):
        store = Store(path=REPO_PATH)
        assert store.name == "path"

    def test_path(self, mock_repo):
        store = Store(path=REPO_PATH)
        assert store.path == REPO_PATH

    def test_edit(self, mock_repo, mock_run):
        with mock.patch("spykes.store.Secret"):
            store = Store(path=REPO_PATH)
            store.edit()
