# import dxchange
import argparse
import textwrap

import dxchange.reader as dxreader
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Slider


def read_txm(file, slices=None):
    data, meta = dxreader.read_txrm(file, slice_range=slices)
    return data, meta


def slice_viewer(data, metadata=None, **kwargs):
    fig = plt.figure(figsize=(10, 8))
    gs = GridSpec(5, 3, figure=fig, height_ratios=[8, 3, 0.2, 0.2, 0.2])
    # image axes
    ax_xy = fig.add_subplot(gs[0, 0])
    ax_xz = fig.add_subplot(gs[0, 1])
    ax_yz = fig.add_subplot(gs[0, 2])
    plt.subplots_adjust(hspace=0.25)
    # plot images
    imxy = ax_xy.imshow(data[data.shape[0] // 2], **kwargs)
    imxz = ax_xz.imshow(data[:, data.shape[1] // 2, :], **kwargs)
    imyz = ax_yz.imshow(data[:, :, data.shape[2] // 2], **kwargs)
    ax_xy.set_title('Top view')
    ax_xz.set_title('Side view')
    ax_yz.set_title('Front view')

    for ax, color in zip([ax_xy, ax_xz, ax_yz], ['green', 'blue', 'red']):
        plt.setp(ax.spines.values(), color=color, linewidth=2)

    # histogram axis
    ax_h = fig.add_subplot(gs[1, :], )
    ax_h.hist((data[data.shape[0] // 2].flatten(), data[:, data.shape[1] // 2, :].flatten(),
               data[:, :, data.shape[2] // 2].flatten()), color=('g', 'b', 'r'), label=('Top', 'Side', 'Front'),
              bins=100)
    ax_h.legend()

    # set up sliders
    axcolor = 'lightgoldenrodyellow'
    axslice_xy = fig.add_subplot(gs[2, :], facecolor=axcolor)
    axslice_xz = fig.add_subplot(gs[3, :], facecolor=axcolor)
    axslice_yz = fig.add_subplot(gs[4, :], facecolor=axcolor)
    sslice_xy = Slider(axslice_xy, 'Slice top', 0, data.shape[0] - 1, valinit=data.shape[0] // 2, valstep=1)
    sslice_xz = Slider(axslice_xz, 'Slice side', 0, data.shape[1] - 1, valinit=data.shape[1] // 2, valstep=1)
    sslice_yz = Slider(axslice_yz, 'Slice front', 0, data.shape[2] - 1, valinit=data.shape[2] // 2, valstep=1)

    # draw lines indicating slices
    def clear_lines():
        for i in range(2):
            ax_xy.mylines[i].remove()
            ax_xz.mylines[i].remove()
            ax_yz.mylines[i].remove()

    def draw_lines(sxy, sxz, syz):
        ax_xy.mylines = []
        ax_xz.mylines = []
        ax_yz.mylines = []
        ax_xy.mylines.append(ax_xy.axhline(int(sxz), alpha=0.5, color='blue'))
        ax_xy.mylines.append(ax_xy.axvline(int(syz), alpha=0.5, color='red'))
        ax_xz.mylines.append(ax_xz.axhline(int(sxy), alpha=0.5, color='green'))
        ax_xz.mylines.append(ax_xz.axvline(int(syz), alpha=0.5, color='red'))
        ax_yz.mylines.append(ax_yz.axhline(int(sxy), alpha=0.5, color='green'))
        ax_yz.mylines.append(ax_yz.axvline(int(sxz), alpha=0.5, color='blue'))

    draw_lines(int(sslice_xy.val), int(sslice_xz.val), int(sslice_yz.val))

    def update(val):
        sxy = int(sslice_xy.val)
        sxz = int(sslice_xz.val)
        syz = int(sslice_yz.val)
        imxy.set_data(data[sxy])
        imxz.set_data(data[:, sxz, :])
        imyz.set_data(data[:, :, syz])

        clear_lines()
        draw_lines(sxy, sxz, syz)

        # Update histograms
        ax_h.clear()
        ax_h.hist((data[sxy], data[:, sxz, :],
                   data[:, :, syz]), color=('g', 'b', 'r'), label=('Top', 'Side', 'Front'), bins=100)
        ax_h.legend()

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

    print('running')
    data, meta = read_txm(args.file)  # ,slices=((0,10,1),(0,1013,1),(0,988,1)))
    slice_viewer(data, cmap='bone')
