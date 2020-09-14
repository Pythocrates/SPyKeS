#! /usr/bin/env python3

''' SPyKeS - your Simple Python Key Storage.
'''

from pathlib import Path

from spykes.parsing import _parse_args
from spykes.store_manager import StoreManager


def main():
    args = _parse_args()
    manager = StoreManager(Path.home() / '.config' / 'spykes')

    if args.subcmd in ['add-store', 'select-store', 'list-stores']:
        func = getattr(manager, args.subcmd.replace('-', '_'))
    elif args.subcmd in ['edit', 'show', 'add-user', 'list-users']:
        store = manager.current_store
        func = getattr(store, args.subcmd.replace('-', '_'))

    args = vars(args)
    del args['subcmd']
    func(**args)
