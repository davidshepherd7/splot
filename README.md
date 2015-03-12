splot -- simple command line plotting
=====================================

A cli utility to easily create plots from text files or piped input.

Based on python's matplotlib.


Full documentation is provided by `splot -h`:

    usage: splot [-h] [--delimiter DELIMITER] [--header] [--transpose]
                 [--stretch-x] [--col COL]
                 [filenames [filenames ...]]
    
    Take two-column dataset and create a simple 2D plot.
    
    positional arguments:
      filenames             Files to plot, - reads from stdin, by default read
                            from stdin
    
    optional arguments:
      -h, --help            show this help message and exit
      --delimiter DELIMITER, -d DELIMITER
                            Set the delimiter, by default use any whitespace.
      --header              Does the file have a header line?
      --transpose
      --stretch-x           Should subsequent files be mapped onto the x range of
                            the first?
      --col COL             Column of the data to plot
