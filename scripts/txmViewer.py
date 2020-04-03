# import dxchange
import argparse
import textwrap

import dxchange.reader as dxreader
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider


def read_txm(file, slices=None):
    data, meta = dxreader.read_txrm(file, slice_range=slices)
    return data, meta


def slice_viewer(data, metadata=None, **kwargs):
    fig, ((ax1, ax2, ax3), (ax4, ax5, ax6)) = plt.subplots(2, 3)
    plt.subplots_adjust(left=0.25, bottom=0.25)
    # plot images
    imxy = ax1.imshow(data[data.shape[0] // 2])
    imxz = ax2.imshow(data[:, data.shape[1] // 2, :])
    imyz = ax3.imshow(data[:, :, data.shape[2] // 2])
    ax1.set_title('Top view')
    ax2.set_title('Side view')
    ax3.set_title('Front view')

    for ax, color in zip([ax1, ax2, ax3], ['black', 'blue', 'red']):
        plt.setp(ax.spines.values(), color=color)
    # plot histograms
    ax4.hist(data[data.shape[0] // 2].flatten())
    ax5.hist(data[:, data.shape[1] // 2, :].flatten())
    ax6.hist(data[:, :, data.shape[2] // 2].flatten())

    # set up slider
    # ax.margins(x=0)
    axcolor = 'lightgoldenrodyellow'
    axslice_xy = plt.axes([0.25, 0.15, 0.65, 0.03], facecolor=axcolor)
    axslice_xz = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    axslice_yz = plt.axes([0.25, 0.05, 0.65, 0.03], facecolor=axcolor)
    sslice_xy = Slider(axslice_xy, 'Slice top', 0, data.shape[0] - 1, valinit=data.shape[0] // 2, valstep=1)
    sslice_xz = Slider(axslice_xz, 'Slice side', 0, data.shape[1] - 1, valinit=data.shape[1] // 2, valstep=1)
    sslice_yz = Slider(axslice_yz, 'Slice front', 0, data.shape[2] - 1, valinit=data.shape[2] // 2, valstep=1)

    # draw lines indicating slices
    def clear_lines():
        for i in range(2):
            ax1.mylines[i].remove()
            ax2.mylines[i].remove()
            ax3.mylines[i].remove()

    def draw_lines(sxy, sxz, syz):
        ax1.mylines = []
        ax2.mylines = []
        ax3.mylines = []
        ax1.mylines.append(ax1.axhline(int(sxz), alpha=0.5, color='blue'))
        ax1.mylines.append(ax1.axvline(int(syz), alpha=0.5, color='red'))
        ax2.mylines.append(ax2.axhline(int(sxy), alpha=0.5, color='black'))
        ax2.mylines.append(ax2.axvline(int(syz), alpha=0.5, color='red'))
        ax3.mylines.append(ax3.axhline(int(sxy), alpha=0.5, color='black'))
        ax3.mylines.append(ax3.axvline(int(sxz), alpha=0.5, color='blue'))

    draw_lines(int(sslice_xy.val), int(sslice_xz.val), int(sslice_yz.val))

    def update(val):
        sxy = int(sslice_xy.val)
        sxz = int(sslice_xz.val)
        syz = int(sslice_yz.val)
        imxy.set_data(data[sxy])
        imxz.set_data(data[:, sxz, :])
        imyz.set_data(data[:, :, syz])

        # Updata histograms
        ax4.clear()
        ax5.clear()
        ax6.clear()
        ax4.hist(data[sxy].flatten())
        ax5.hist(data[:, sxz, :].flatten())
        ax6.hist(data[:, :, syz].flatten())

        clear_lines()
        draw_lines(sxy, sxz, syz)
        fig.canvas.draw_idle()

    sslice_xy.on_changed(update)
    sslice_xz.on_changed(update)
    sslice_yz.on_changed(update)

    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='txmViewer',
        description='Reads the data from a txm file and create an interactive plot of slices\n ',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''
                python txmViewer file -keywords --options
                ''')
    )
    parser.add_argument(
        '-f', '--file', type=str, help='path to txm file',
        default='/home/hektor/Downloads/granges_treated_60kV_le3_1100nm_recon006.txm'
    )
    args = parser.parse_args()

    data, meta = read_txm(args.file)  # ,slices=((0,10,1),(0,1013,1),(0,988,1)))
    slice_viewer(data)
