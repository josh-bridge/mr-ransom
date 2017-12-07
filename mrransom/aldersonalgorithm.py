from cipher.caeser import CaeserCipher
from cipher.reverse import ReverseCipher
from cipher.vernam import VernamCipher
import locksmith

ENCRYPT = 'encrypt'

DECRYPT = 'decrypt'


def caeser(message, key, mode):
    return CaeserCipher(locksmith.caeser_key(key)).process(message, mode)


def reverse(message):
    return ReverseCipher.process(message)


def vernam(message, key):
    return VernamCipher(key.string).process(message)


def get_blocks(message, n=4):
    return [message[i:i+n] for i in range(0, len(message), n)]


def encrypt_block(message, key):
    step_1 = caeser(message, key, ENCRYPT)

    step_2 = reverse(step_1)

    return vernam(step_2, key)


def decrypt_block(message, key):
    step_1 = vernam(message, key)

    step_2 = reverse(step_1)

    return caeser(step_2, key, DECRYPT)


class AldersonAlgorithm:

    def __init__(self, key):
        self.key = key

    def encrypt(self, message):
        message_blocks = get_blocks(message)
        encrypted = []
        key = self.key

        for i in range(len(message_blocks)):
            block = encrypt_block(message_blocks[i], key)
            encrypted.append(block)

            if i > 0:
                key = locksmith.rotate_key(key, block)

        return ''.join(encrypted)

    def decrypt(self, message):
        message_blocks = get_blocks(message)
        decrypted = []
        key = self.key

        for i in range(len(message_blocks)):
            block = message_blocks[i]
            decrypted.append(decrypt_block(block, key))

            if i > 0:
                key = locksmith.rotate_key(key, block)

        return ''.join(decrypted)
