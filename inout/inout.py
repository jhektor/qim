import dxchange.reader as dxreader
import dxchange.writer as dxwriter

def read_txm(file, slices=None):
    data, meta = dxreader.read_txrm(file, slice_range=slices)
    return data, meta

def merge_tiffs(fname,output,ind):
    print('Reading data')
    data = dxreader.read_tiff_stack(fname, ind)
    print('Saving merged data to {}'.format(output))
    dxwriter.write_tiff(data,fname=output)

def save_tiff(data,output):
    print('Saving data to {}'.format(output))
    dxwriter.write_tiff(data,fname=output)