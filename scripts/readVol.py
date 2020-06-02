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

def crop_slices(volume, start,stop,step=1):
    return volume[start:stop:step]    

def read_vol(fname, info=None, dims = None, crop = None, uint16=False):
    if info:
        dims=parse_info(info)
    d = np.fromfile(fname,dtype=np.float32)
    volume = d.reshape(dims)
    if crop:
        volume = crop_slices(volume, *crop)
    if uint16:
        volume = convert_to_uint16(volume)
    return volume


def convert_to_uint16(volume):
    # scale to values in 0-65535
    Imin = volume.min()
    Imax = volume.max()
    a = 65535./(Imax-Imin)
    b = 65535 - a*Imax
    return (a*volume+b).astype(np.uint16)

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
    parser.add_argument(
        '-c', '--crop' , type=int, nargs=3, help='first last step for cropping slices'
    )
    parser.add_argument(
        '--uint16' , default=False, action="store_true", help='convert output to uint16'
    )
    args = parser.parse_args()
    if args.info:
        vol=read_vol(args.fname,info=args.info, crop=args.crop, uint16=args.uint16)
    elif args.dims:
        vol=read_vol(args.fname,dims=args.dims, crop=args.crop, uint16=args.uint16)
    else:
        print('Must supply either a .info file or dimension of volume')
        exit
    save_to_tiff(vol,args.output)