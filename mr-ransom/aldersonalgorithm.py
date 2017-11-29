import base64

from cipher.caeser import CaeserCipher
from cipher.reverse import ReverseCipher

ENCRYPT = 'encrypt'

DECRYPT = 'decrypt'


def process(key, in_text, mode):
    step_1 = CaeserCipher(key).process(in_text, mode)

    step_2 = ReverseCipher.process(step_1)

    return step_2


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
