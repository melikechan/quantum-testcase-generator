import os
import sys
import logging
import argparse


def main(args=None):
    argparser = argparse.ArgumentParser()

    argparser.add_argument('inputfile', type=str, help='Input file')
    argparser.add_argument('outputdir', type=str, help='Output directory')
    argparser.add_argument('-n', type=int, help='Number of testcases')

    args = argparser.parse_args(args)

    logging.basicConfig(level=logging.INFO)

    logging.info(f'Input file: {args.inputfile}')
    logging.info(f'Output directory: {args.outputdir}')
    logging.info(f'Number of testcases: {args.n}')

    # Validate files
    if not os.path.isfile(args.inputfile):
        logging.error(f'Input file {args.inputfile} not found')
        return 1

    if not os.path.isdir(args.outputdir):
        os.mkdir(args.outputdir)
        logging.info(f'Output directory {args.outputdir} created')
    else:
        logging.info(f'Output directory {args.outputdir} exists')

    if args.n is None:
        logging.info('Default number of testcases: 1')
        args.n = 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
