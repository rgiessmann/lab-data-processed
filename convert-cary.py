#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Transform cary300 data
"""

import configargparse
import logging
import os
import sys


import pandas

logging.basicConfig(format="%(asctime)s [%(levelname)-5.5s]  %(message)s", level=logging.INFO)


def self_log():
    ####################### header version 2019-04-03 ####################
    import hashlib
    import io
    import os
    import sys
    import shutil

    with open(__file__, "rb") as f:
        digest = hashlib.file_digest(f, "sha256")

    _mypath = os.path.abspath(__file__)
    _mysha256sum = digest.hexdigest()
    _myfilename = os.path.basename(__file__)

    logger = logging.getLogger(__name__)
    logger.info("Hi, this is: '{}' as '{}'".format(_myfilename, __name__))
    logger.info("I am located here:")
    logger.info(_mypath)
    logger.info("My sha256sum hash is:")
    logger.info(_mysha256sum)
    ######################################################################
self_log()

## end of header

def main(argv=None):
    logger = logging.getLogger(__name__)

    if argv is None:
        argv = sys.argv[1:]

    parser = configargparse.ArgParser()

    parser.add_argument(dest="filenames", metavar="<file_to_split>", nargs="+", help="")
    parser.add_argument("-s", "--separator", action="store_true", help="changes the decimal separator from comma (1,29) to point (1.29)")
    parser.add_argument('-v', '--verbose', dest='debug', action='store_true', help='Show verbose information.')
    parser.add_argument('-n', '--not_in_place',action='store_true', help='Saves output files into current directory instead of the original path.')

    ## processes args from ArgumentParser
    args = parser.parse_args(argv)

    if args.debug:
        logger.setLevel(logging.DEBUG)

    filenames = args.filenames
    decimal_separator = "." if args.separator else ","
    not_in_place = args.not_in_place

    logger.info("Processing files...")

    for filename in filenames:
        logger.debug(f"Acting on file {filename}...")

        with open(filename) as f:
            lines = f.readlines()
            assert lines[1] == "Wavelength (nm),Abs,\n"
            empty_lines = list([i for (i, line) in enumerate(lines) if line == "\n"])
            assert len(empty_lines) == 2
            assert len(lines)-1 in empty_lines
            empty_lines.remove(len(lines)-1)
            skip_footer = len(lines)-empty_lines[0]

        df = pandas.read_csv(filename, skiprows=1, skipfooter=skip_footer, engine="python")
        df = df.rename(columns={"Wavelength (nm)": "Wavelength"})

        new_filename = os.path.splitext(filename)[0] + ".tsv"
        if not_in_place:
            new_filename = "./" + os.path.splitext(os.path.basename(filename))[0] + ".tsv"

        df.to_csv(new_filename, sep="\t", columns=["Wavelength", "Abs"], index=False, decimal=decimal_separator)
    logger.debug("... done.")

if __name__ == "__main__":
    main()
