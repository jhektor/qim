import argparse
import textwrap
import numpy as np
import dxchange.writer as dxwriter


def parse_info(fname):
    with open(fname,'r') as f:
        lines = f.readlines()

    for l in lines:
        if l.startswith('NUM_X'):
            x = int(l.split('=')[-1])
        elif l.startswith('NUM_Y'):
            y = int(l.split('=')[-1])
        elif l.startswith('NUM_Z'):
            z = int(l.split('=')[-1])
    return (z,y,x)
    

def read_vol(fname, info=None, dims = None):
    if info:
        dims=parse_info(info)
    d = np.fromfile(fname,dtype=np.float32)
    volume = d.reshape(dims)
    return volume

def save_to_tiff(data,output):
    dxwriter.write_tiff(data,fname=output)
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog='readVol',
        description='Read a .vol file and convert it to a .tiff \n ',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
                python readVol.py fname output -keywords --options
                ''')
    )
    parser.add_argument(
        'fname',  type=str, help='Name of the input .vol file'
    )
    parser.add_argument(
        'output', type=str, help='Name of output .tiff file file'
    )
    parser.add_argument(
        '-i', '--info' , type=str, help='Name of PyHST info file'
    )
    parser.add_argument(
        '-d', '--dims' , type=int, nargs=3, help='x y z coordinates of volume'
    )
    args = parser.parse_args()
    if args.info:
        vol=read_vol(args.fname,info=args.info)
    elif args.dims:
        vol=read_vol(args.fname,dims=args.dims)
    else:
        print('Must supply either a .info file or dimension of volume')
        exit
    save_to_tiff(vol,args.output)