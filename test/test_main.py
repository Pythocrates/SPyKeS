''' This test the main function.
'''

import sys
from unittest import mock

from spykes.spk import main


class TestMain:
    @staticmethod
    def test_list_stores():
        with mock.patch('spykes.spk.StoreManager') as sm_mock:
            sm_mock.current_store = mock.PropertyMock()
            sys.argv = ['X', 'list-stores']
            main()
            assert sm_mock.called

    @staticmethod
    def test_edit():
        with mock.patch('spykes.spk.StoreManager') as sm_mock:
            sm_mock.current_store = mock.PropertyMock()
            sys.argv = ['X', 'edit']
            main()
            assert sm_mock.called
