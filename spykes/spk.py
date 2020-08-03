#! /usr/bin/env python3

''' SPyKeS - your Simple Python Key Storage.
'''

from argparse import ArgumentParser
from pathlib import Path

from spykes.store_manager import StoreManager


def _parse_args():
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest='subparser_name')
    subparsers.add_parser('edit')
    subparsers.add_parser('show')
    subparsers.add_parser('add-user')
    subparsers.add_parser('list-users')

    asp = subparsers.add_parser('add-store')
    asp.add_argument('name')
    asp.add_argument('url')
    asp.add_argument(
        '--initial-key', '-i', required=False, type=Path,
        help='initialize using given public key and empty keys file',
    )

    ssp = subparsers.add_parser('select-store')
    ssp.set_defaults(name='select-store')
    ssp.add_argument('name')

    subparsers.add_parser('list-stores')

    return parser.parse_args()


def main():
    args = _parse_args()
    manager = StoreManager(Path.home() / '.config' / 'spykes')
    if args.subparser_name in ['add-store', 'select-store', 'list-stores']:
        func = getattr(manager, args.subparser_name.replace('-', '_'))
    elif args.subparser_name in ['edit', 'show', 'add-user', 'list-users']:
        store = manager.current_store
        func = getattr(store, args.subparser_name.replace('-', '_'))
    else:
        raise Exception(f'Unhandled subparser {args.subparser_name}.')

    args = vars(args)
    del args['subparser_name']
    func(**args)


if __name__ == '__main__':
    main()