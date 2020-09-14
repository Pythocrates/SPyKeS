''' This module helps with parsing command-line arguments.
'''

from argparse import ArgumentParser
from pathlib import Path


def _parse_args():
    parser = ArgumentParser()

    subparsers = parser.add_subparsers(dest='subcmd')
    subparsers.add_parser('edit')
    subparsers.add_parser('show')
    aup = subparsers.add_parser('add-user')
    aup.add_argument(
        'public_key', type=Path, metavar='public-key',
        help='the public key for the new user',
    )
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
    subparsers.required = True

    return parser.parse_args()
