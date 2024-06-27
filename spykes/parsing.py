"""
This module helps with parsing command-line arguments.
"""

from argparse import ArgumentParser
from pathlib import Path


class AddUserArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, description="Add a new key store user.")
        self.add_argument(
            "key_path",
            metavar="key-path",
            type=Path,
            help="Path to the user's GPG key file.",
        )


class AddStoreArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, description="Add a new key store.")
        self.add_argument("name")
        self.add_argument(
            "repository_url",
            metavar="repository-url",
            help="URL of a remote store repository.",
        )
        self.add_argument(
            "--initial-public-key",
            "-i",
            required=False,
            type=Path,
            help="Initialize using given public key and empty keys file.",
        )


class SelectStoreArgumentParser(ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, description="Select an existing key store.")
        self.add_argument("name")
