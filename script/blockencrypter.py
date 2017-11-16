from threading import Thread
from cipher.caeser import CaeserCipher

DEFAULT_BLOCK_SIZE = 500 * 1024


def get_blocks(file_bytes, block_size=DEFAULT_BLOCK_SIZE):
    blocks = []

    file_size = len(file_bytes)
    if file_size > block_size:
        total_blocks = float(file_size) / float(block_size)
        current_block = 0

        while total_blocks > 0.0:
            blocks.append(file_bytes[current_block:])
            current_block = current_block + block_size
            total_blocks = total_blocks - 1.0
    else:
        blocks.append(file_bytes)

    return blocks


def close_threads(workers):
    for process in workers:
        process.join()
        workers.remove(process)


class BlockEncrypter:

    def __init__(self, chunks, key):
        self.blocks = chunks
        self.key = key

    def process(self, mode):
        block_num = 0
        workers = []
        processed = [""]*len(self.blocks)

        for block in self.blocks:
            process = Thread(target=self.process_block, args=(processed, block, block_num, mode, self.key))
            workers.append(process)
            process.start()

            block_num = block_num + 1

        close_threads(workers)

        return "".join(processed)

    @staticmethod
    def process_block(processed, block, block_num, mode, key):
        processed[block_num] = CaeserCipher(key, mode).process(block)
