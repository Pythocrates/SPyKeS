''' This test the command-line parsing.
'''

import sys

import pytest

from spykes.parsing import _parse_args


class TestParsing:
    @staticmethod
    def test_edit():
        sys.argv = ['X', 'edit']
        args = _parse_args()
        assert vars(args) == {'subcmd': 'edit'}

    @staticmethod
    def test_no_args(capsys):
        sys.argv = ['X']
        with pytest.raises(SystemExit):
            _parse_args()
        captured = capsys.readouterr()
        assert captured.err.startswith('usage:')
