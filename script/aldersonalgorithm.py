import base64

from cipher.caeser import CaeserCipher

ENCRYPT = 'encrypt'

DECRYPT = 'decrypt'


def process(key, in_text, mode):
    return CaeserCipher(key, mode).process(in_text)


def xor_string(string1, string2):
    arr1 = [ord(c) for c in string1]
    arr2 = [ord(c) for c in string2]

    arr3 = []
    for i in range(len(arr1)):
        arr3.append(arr1[i] ^ arr2[i])

    return "".join(map(chr, arr3))


class AldersonAlgorithm:
    def __init__(self, key):
        self.key = key
        self.previous = None

    def encrypt_chunk(self, chunk):
        result = process(self.key, base64.b64encode(chunk), ENCRYPT)

        if self.previous is not None:
            result = xor_string(result, self.previous)

        self.previous = result
        return result

    def decrypt_chunk(self, chunk):
        result = process(self.key, chunk, DECRYPT)

        if self.previous is not None:
            result = xor_string(result, self.previous)

        self.previous = result
        return base64.b64decode(result)
