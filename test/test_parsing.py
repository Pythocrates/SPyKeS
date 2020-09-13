''' This test the command-line parsing.
'''

import sys

from spykes.parsing import _parse_args


class TestParsing:
    @staticmethod
    def test_edit():
        sys.argv = ['X', 'edit']
        args = _parse_args()
        assert vars(args) == {'subparser_name': 'edit'}

    @staticmethod
    def test_no_args(capsys):
        sys.argv = ['X']
        _parse_args()
        captured = capsys.readouterr()
        assert captured.out.startswith('usage:')
