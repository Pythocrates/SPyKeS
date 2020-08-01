#! /usr/bin/env python3

''' SPyKeS - your Simple Python Key Storage.
'''

from argparse import ArgumentParser
from pathlib import Path

from spykes.store import Store


def _parse_args():
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='subparser_name')

    subparsers.add_parser('edit')
    subparsers.add_parser('show')

    return parser.parse_args()


def main():
    args = _parse_args()
    store = Store(path=Path.home() / 'clones' / 'simple-keystore')
    getattr(store, args.subparser_name)()


if __name__ == '__main__':
    main()
