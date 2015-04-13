#! /usr/bin/python3

import sys
import argparse
import numpy as np

from matplotlib.pyplot import show as pltshow
from matplotlib.pyplot import subplots

def open_or_stdin(filename, *args, **kwargs):
    if filename == "-":
        return sys.stdin
    else:
        return open(filename, *args, **kwargs)


def main():
    """Take two-column dataset and create a simple 2D plot.

    """

    # Parse args
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument('--delimiter', '-d', default=None,
                        help="Set the delimiter, by default use any whitespace.")
    parser.add_argument('--header', action="store_true",
                        help="Does the file have a header line?")
    parser.add_argument('filenames', nargs="*", default=["-"],
                        help="Files to plot, - reads from stdin, by default read from stdin")
    parser.add_argument('--transpose', '-t', action="store_true",
                        help="Transpose data before plotting")
    parser.add_argument('--stretch-x',  action = "store_true",
                        help = "Should subsequent files be mapped onto the x range of the first?")
    parser.add_argument('--col',  default = None,
                        help = "Column of the data to plot")
    args = parser.parse_args()


    # Make plot
    fig, ax = subplots(1, 1)

    xmin = None
    xmax = None

    # Read and plot data
    for name in args.filenames:
        with open_or_stdin(name, 'r') as f:

            if args.header:
                header = f.readline()
            else:
                header = None

            data = []
            for line in f.readlines():
                l = [float(x) for x in line.strip().split(args.delimiter)]
                data.append(l)

        data = np.array(data)

        if args.col is not None:
            data = data[:, args.col]

        if args.transpose:
            data = np.transpose(data)

        if args.stretch_x and xmin is None and xmax is None:
            xmin = 0
            xmax = len(data)


        if args.stretch_x:
            ax.plot(np.linspace(xmin, xmax, len(data)), data, label = name)
        else:
            ax.plot(data, label=name)

    ax.legend(loc=0)

    pltshow()


if __name__ == '__main__':
    sys.exit(main())