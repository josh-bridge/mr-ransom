# Reverse Cipher (slightly modified)
# http://inventwithpython.com/hacking (BSD Licensed)


class ReverseCipher:

    def __init__(self):
        pass

    @staticmethod
    def process(message):
        translated = ''

        i = len(message) - 1
        while i >= 0:
            translated += message[i]
            i = i - 1

        return translated
