# Caesar Cipher
# http://inventwithpython.com/hacking (BSD Licensed)

VALID_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
DECRYPT = 'decrypt'
ENCRYPT = 'encrypt'


def format_key(key_ints):
    new_key = 0
    for c in key_ints:
        new_key = new_key ^ c
    return new_key


class CaeserCipher:

    def __init__(self, key):
        self.key = format_key(key.ints)

    def process(self, message, mode):
        # stores the encrypted/decrypted form of the message
        translated = ''

        # run the encryption/decryption code on each symbol in the message string
        for char in message:
            if char in VALID_LETTERS:
                # get the encrypted (or decrypted) number for this symbol
                num = VALID_LETTERS.find(char)  # get the number of the symbol

                if mode == ENCRYPT:
                    num += self.key
                elif mode == DECRYPT:
                    num -= self.key

                # handle the wrap-around if num is larger than the length of
                # valid_letters or less than 0
                if num >= len(VALID_LETTERS):
                    num -= len(VALID_LETTERS)
                elif num < 0:
                    num += len(VALID_LETTERS)

                # add encrypted/decrypted number's symbol at the end of translated
                translated = translated + VALID_LETTERS[num]

            else:
                # just add the symbol without encrypting/decrypting
                translated = translated + char

        return translated
