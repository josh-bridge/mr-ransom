import base64

from cipher.caeser import CaeserCipher


def process(key, in_text, mode):
    return CaeserCipher(key, mode).process(in_text)


class AldersonAlgorithm:
    def __init__(self, key):
        self.key = key

    def encrypt_chunk(self, in_text):
        return process(self.key, base64.b64encode(in_text), 'encrypt')

    def decrypt_chunk(self, in_text):
        return base64.b64decode(process(self.key, in_text, 'decrypt'))

