from cipher.caeser import CaeserCipher
from cipher.reverse import ReverseCipher
from cipher.vernam import VernamCipher
import locksmith

ENCRYPT = 'encrypt'

DECRYPT = 'decrypt'


class AldersonAlgorithm:

    def __init__(self, key):
        self.key = key

    def encrypt(self, message):
        step_1 = CaeserCipher(locksmith.caeser_key(self.key)).process(message, ENCRYPT)

        step_2 = ReverseCipher.process(step_1)

        return VernamCipher(self.key.string).process(step_2)

    def decrypt(self, message):
        step_1 = VernamCipher(self.key.string).process(message)

        step_2 = ReverseCipher.process(step_1)

        return CaeserCipher(locksmith.caeser_key(self.key)).process(step_2, DECRYPT)
