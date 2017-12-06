# Caesar Cipher (slightly modified)
# http://inventwithpython.com/hacking (BSD Licensed)

VALID_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' \
                'abcdefghijklmnopqrstuvwxyz' \
                '0123456789+/='

DECRYPT = 'decrypt'
ENCRYPT = 'encrypt'


class CaeserCipher:

    def __init__(self, key):
        self.key = key

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
                num = self.wrap(num)

                # add encrypted/decrypted number's symbol at the end of translated
                translated = translated + VALID_LETTERS[num]

            else:
                # just add the symbol without encrypting/decrypting
                translated = translated + char

        return translated

    def wrap(self, num):
        changed = True
        new_num = num

        while changed:
            changed = False
            if new_num >= len(VALID_LETTERS):
                new_num -= len(VALID_LETTERS)
                changed = True
            elif new_num < 0:
                new_num += len(VALID_LETTERS)
                changed = True

        return new_num
