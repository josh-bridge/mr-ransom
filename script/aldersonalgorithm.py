import base64

from cipher.caeser import CaeserCipher

ENCRYPT = 'encrypt'

DECRYPT = 'decrypt'


def process(key, in_text, mode):
    return CaeserCipher(key, mode).process(in_text)


class AldersonAlgorithm:
    def __init__(self, key):
        self.key = key
        self.previous = ""

    def encrypt_chunk(self, chunk):
        result = process(self.key, base64.b64encode(chunk), ENCRYPT)
        self.previous = result

        return result

    def decrypt_chunk(self, chunk):
        result = base64.b64decode(process(self.key, chunk, DECRYPT))
        self.previous = result

        return result

    def encrypt_file(self, file_path, out_file_path):
        pass

    def decrypt_file(self, file_path, out_file_path):
        pass

