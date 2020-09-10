''' This test the command-line parsing.
'''

import sys

import pytest

from spykes.parsing import _parse_args


class TestParsing:
    def test_edit(self):
        sys.argv = ['X', 'edit']
        args = _parse_args()
        assert vars(args) == {'subparser_name': 'edit'}

    def test_no_args(self, capsys):
        sys.argv = ['X']
        args = _parse_args()
        captured = capsys.readouterr()
        assert captured.out.startswith('usage:')
