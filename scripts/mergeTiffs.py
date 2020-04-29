import argparse
import textwrap

import dxchange.reader as dxreader
import dxchange.writer as dxwriter
import numpy as np

def merge_tiffs(args):
    print('Reading data')
    data = dxreader.read_tiff_stack(args.fname, args.ind)
    print('Saving merged data to {}'.format(args.output))
    dxwriter.write_tiff(data,fname=args.output)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='mergeTiffs',
        description='Merges tiff files into a single file \n ',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
                python mergeTiffs.py fname output first last -keywords --options
                ''')
    )
    parser.add_argument(
        'fname',  type=str, help='Name of one of the files in the stack'
    )
    parser.add_argument(
        'output', type=str, help='Name of merged tiff volume file'
    )
    parser.add_argument(
        'first', type=int, help='Index of first image'
    )
    parser.add_argument(
        'last', type=int, help='Index of last image'
    )
    parser.add_argument(
        '-s', '--step' , type=int, default=1, help='Step size for reading images'
    )
    args = parser.parse_args()
    args.ind = np.arange(args.first,args.last+1,args.step)

    merge_tiffs(args)
    
    
