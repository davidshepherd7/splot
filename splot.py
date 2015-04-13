#! /usr/bin/python3

import sys
import argparse
import numpy as np
import re

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
    parser.add_argument('--col',  default = None, type = int,
                        help = "Column of the data to plot")
    parser.add_argument('--use-x', action = "store_true",
                        help = "Use first column of data as x values")
    args = parser.parse_args()


    # Make plot
    fig, ax = subplots(1, 1)

    xmin = None
    xmax = None

    # Read and plot data
    for name in args.filenames:
        with open_or_stdin(name, 'r') as f:

            # Check the first line, if it's text then treat it as a header
            maybe_header = f.readline()
            ncol = len(maybe_header.strip().split(args.delimiter))

            # Get headers
            if args.transpose:
                # Fill in later
                headers = []
                start_line = [maybe_header]

            elif re.match('^[A-Za-z]', maybe_header) or args.header:
                headers = maybe_header.strip().split(args.delimiter)
                start_line = []

            else:
                headers = [str(i) for i in range(0, ncol)]
                start_line = [maybe_header]


            # Read data
            data = []
            for line in start_line + f.readlines():
                line = line.strip().split(args.delimiter)

                if args.transpose and args.header:
                    headers.append(line[0])
                    line = line[1:]

                l = [float(x) for x in line]
                data.append(l)

        data = np.array(data)
        if args.transpose:
            data = np.transpose(data)

        # If we said to, then use the first col as x values
        if args.use_x:
            x_data = data[:, 0]
            x_label = headers[0]
            y_data = data[:, 1:]
            y_label = headers[1]
        else:
            x_label = "Number"
            x_data = range(0, data.shape[0])
            y_data = data
            y_label = headers[0]

        # Maybe pick some specific cols for the y values
        if args.col is not None:
            y_data = y_data[:, args.col]
            y_label = headers[args.col]


        # Maybe stretch the data to fit the first files x scale
        if args.stretch_x and xmin is None and xmax is None:
            xmin = min(x_data)
            xmax = max(x_data)
        elif args.stretch_x:
            x_data = rescale(x_data, xmin, xmax)

        ax.plot(x_data, y_data, label = name)

    ax.legend(loc=0)

    pltshow()


def rescale(data, minv, maxv):
    data = np.array(data)

    # map to [0,1]
    data = (data - min(data)) / (max(data) - min(data))

    # map to [minv, maxv]
    data = data * (maxv - minv) +  minv

    return data


def rescale_test():

    def assert_almost_equal(a, b, tol=1e-9):
        assert(abs(a - b) < tol)

    def rescale_check(x, minv, maxv):
        x_r = rescale(x, minv, maxv)
        assert_almost_equal(max(x_r), maxv)
        assert_almost_equal(min(x_r), minv)

    tests = [
        # Basic
        [[1, 2, 3, 4, 5.0], 1, 2],

        # Negative values
        [[1, 2, 3, 4, 5.0], -5.1, 2.5],
        [[1, 2, 3, 4, 5.0], -5.1,- 2.5],
        [[ -1, 0, 2, 4, 5.0], 1, 2],

        # More with floats
        [[1, 2, 3, 4, 5.0], 1, 2.5],
        [[ -1.4125, 0, 2, 4, 5.120983], 1, 2],
    ]


    for x, minv, maxv in tests:
        yield rescale_check, x, minv, maxv


if __name__ == '__main__':
    sys.exit(main())
