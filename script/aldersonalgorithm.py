import base64

from cipher.caeser import CaeserCipher

ENCRYPT = 'encrypt'

DECRYPT = 'decrypt'


def process(key, in_text, mode):
    return CaeserCipher(key, mode).process(in_text)


def format_key(raw_key):
    new_key = 0
    for c in raw_key:
        new_key = new_key ^ c
    return new_key


class AldersonAlgorithm:
    def __init__(self, key):
        self.key = format_key(key)
        self.previous = ""

    def encrypt_chunk(self, chunk):
        result = process(self.key, base64.b64encode(chunk), ENCRYPT)
        self.previous = result

        return result

    def decrypt_chunk(self, chunk):
        result = base64.b64decode(process(self.key, chunk, DECRYPT))
        self.previous = result

        return result

