class VernamCipher:

    def __init__(self, key):
        self.key = key

    def process(self, text):
        result = ""
        ptr = 0
        for char in text:
            result = result + chr(ord(char) ^ ord(self.key[ptr]))
            ptr = ptr + 1
            if ptr == len(self.key):
                ptr = 0

        return result
