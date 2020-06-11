import argparse
import textwrap

import numpy as np

import sys
sys.path.insert(0, '/lunarc/nobackup/projects/qim')
from qim.inout import *
from skimage import img_as_uint

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='txm2tiff',
        description='Reads the data from a txm file and converts it to a tiff image\n ',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
                python txm2tiff txm output -keywords --options
                ''')
    )
    parser.add_argument(
        'txm', type=str, help='path to txm file',
    )
    parser.add_argument(
        'output', type=str, help='path to output tiff file',
    )
    args = parser.parse_args()

    print('Reading {}'.format(args.txm))
    txm, meta = read_txm(args.txm)
    print('Casting to uint16')
    txm = txm.astype('uint16')

    print('Saving to {}'.format(args.output))
    save_tiff(txm,args.output)