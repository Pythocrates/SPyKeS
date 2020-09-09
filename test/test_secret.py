''' This tests the Secret class.
'''

from pathlib import Path

from spykes.secret import Secret


class TestSecret:
    def test_path(self):
        path_1 = Path('/my/path')
        path_2 = Path('/my/path/2')
        secret = Secret(path=path_1, user_keys_path=path_2)
        assert secret.path == path_1
        assert secret._user_keys_path == path_2
