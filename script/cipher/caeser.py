# Caesar Cipher
# http://inventwithpython.com/hacking (BSD Licensed)


class CaeserCipher:

    VALID_LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/='
    DECRYPT = 'decrypt'
    ENCRYPT = 'encrypt'

    def __init__(self, key, mode):
        self.key = key
        self.mode = mode

    def process(self, message):
        # stores the encrypted/decrypted form of the message
        translated = ''

        # run the encryption/decryption code on each symbol in the message string
        for char in message:
            if char in self.VALID_LETTERS:
                # get the encrypted (or decrypted) number for this symbol
                num = self.VALID_LETTERS.find(char)  # get the number of the symbol
                if self.mode == self.ENCRYPT:
                    num = num + self.key
                elif self.mode == self.DECRYPT:
                    num = num - self.key

                # handle the wrap-around if num is larger than the length of
                # valid_letters or less than 0
                if num >= len(self.VALID_LETTERS):
                    num = num - len(self.VALID_LETTERS)
                elif num < 0:
                    num = num + len(self.VALID_LETTERS)

                # add encrypted/decrypted number's symbol at the end of translated
                translated = translated + self.VALID_LETTERS[num]

            else:
                # just add the symbol without encrypting/decrypting
                translated = translated + char

        return translated
