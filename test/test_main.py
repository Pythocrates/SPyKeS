''' This test the main function.
'''

import sys
from unittest import mock

from spykes.spk import main


class TestMain:
    def test_list_stores(self):
        with mock.patch('spykes.spk.StoreManager') as sm:
            sm.current_store = mock.PropertyMock()
            sys.argv = ['X', 'list-stores']
            main()
            assert sm.called

    def test_edit(self):
        with mock.patch('spykes.spk.StoreManager') as sm:
            sm.current_store = mock.PropertyMock()
            sys.argv = ['X', 'edit']
            main()
            assert sm.called
