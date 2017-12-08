import locksmith
from cipher.caeser import CaeserCipher
from cipher.reverse import ReverseCipher
from cipher.vernam import VernamCipher

DEFAULT_BLOCK_SIZE = 5


def get_blocks(message, block_size):
    return [message[i:i + block_size] for i in range(0, len(message), block_size)]


def encrypt_block(message, key):
    step_1 = CaeserCipher(locksmith.caeser_key(key)).process(message, 'encrypt')

    step_2 = ReverseCipher.process(step_1)

    return VernamCipher(key.string).process(step_2)


def decrypt_block(message, key):
    step_1 = VernamCipher(key.string).process(message)

    step_2 = ReverseCipher.process(step_1)

    return CaeserCipher(locksmith.caeser_key(key)).process(step_2, 'decrypt')


class AldersonAlgorithm:

    def __init__(self, key, block_size=DEFAULT_BLOCK_SIZE):
        self.key = key
        self.block_size = block_size

    def encrypt(self, message):
        message_blocks = get_blocks(message, self.block_size)
        encrypted_blocks = []
        key = self.key

        for i in range(len(message_blocks)):
            cipher_block = encrypt_block(message_blocks[i], key)
            encrypted_blocks.append(cipher_block)

            if i > 0:
                key = locksmith.rotate_key(key, cipher_block)

        return ''.join(encrypted_blocks)

    def decrypt(self, message):
        message_blocks = get_blocks(message, self.block_size)
        decrypted_blocks = []
        key = self.key

        for i in range(len(message_blocks)):
            cipher_block = message_blocks[i]
            decrypted_blocks.append(decrypt_block(cipher_block, key))

            if i > 0:
                key = locksmith.rotate_key(key, cipher_block)

        return ''.join(decrypted_blocks)
