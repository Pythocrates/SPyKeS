#! /usr/bin/env python3

"""
SPyKeS - your Simple Python Key Storage.
"""

from .parsing import AddStoreArgumentParser, AddUserArgumentParser, SelectStoreArgumentParser
from .store_manager import StoreManager


def edit_keys(store=StoreManager.get_default().current_store):
    store.edit()


def show_keys(store=StoreManager.get_default().current_store):
    store.show()


def add_user(store=StoreManager.get_default().current_store):
    store.add_user(**vars(AddUserArgumentParser().parse_args()))


def list_users(store=StoreManager.get_default().current_store):
    store.list_users()


def add_store(manager=StoreManager.get_default()):
    manager.add_store(**vars(AddStoreArgumentParser().parse_args()))


def list_stores(manager=StoreManager.get_default()):
    manager.list_stores()


def select_store(manager=StoreManager.get_default()):
    manager.select_store(**vars(SelectStoreArgumentParser().parse_args()))
