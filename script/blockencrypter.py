from threading import Thread
from cipher.caeser import CaeserCipher


def close_threads(workers):
    for process in workers:
        process.join()
        workers.remove(process)


class BlockEncrypter:

    def __init__(self):
        pass

    @staticmethod
    def process(chunk, mode, key):
        return CaeserCipher(key, mode).process(chunk)
