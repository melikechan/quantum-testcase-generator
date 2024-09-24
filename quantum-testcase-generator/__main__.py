import generators
import parser

import os
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

    generate_testcases(args.inputfile, args.outputdir, args.n)

    return 0


def generate_testcases(inputfile, outputdir, test_case_count):
    input_parser = parser.Parser(inputfile)
    data = input_parser.parse().sort(key=lambda x: x['lineNumber'])

    # Singleton generators
    single_number_generator = generators.SingleNumberGenerator(
        l=-10**9, r=10**9)
    tuple_generator = generators.TupleGenerator(
        l=-10**9, r=10**9, num_numbers=2)
    array_generator = generators.ArrayGenerator(
        l=-10**9, r=10**9, num_numbers=5)
    graph_generator = generators.GraphGenerator(n=0, m=0)

    for i in range(test_case_count):
        logging.info(f'Generating testcase {i+1}...')

        variables = {}
        outputfile = os.path.join(outputdir, f'testcase_{i+1}.txt')
        current_line = 1
        for d in data:
            while d['lineNumber'] > current_line:
                os.write(outputfile, '\n')
                current_line += 1

            if d['type'] == 'single':
                args = d['args']

                if d['dataType'] is None:
                    data_type = 'int'
                elif d['dataType'] not in ['int', 'float', 'str']:
                    logging.error(f'Invalid data type {d["dataType"]}:')
                    raise Exception('Invalid data type')
                else:
                    data_type = d['dataType']

                if data_type != 'str':
                    lower_bound = args['valueLowerBound']
                    upper_bound = args['valueUpperBound']

                    variables[d['name']] = single_number_generator.generate(
                        data_type, lower_bound, upper_bound)
                else:
                    # Char generator not implemented yet
                    raise NotImplementedError(
                        'Char generator is not implemented yet')

                os.write(outputfile, f'{variables[d["name"]]} ')
            elif d['type'] == 'tuple':
                pass
            elif d['type'] == 'array':
                pass
            elif d['type'] == 'graph':
                pass
            else:
                logging.error(f'Invalid type {d["type"]}')
                raise Exception('Invalid type')

        logging.info(f'Testcase {i+1} generated: {outputfile}')


if __name__ == '__main__':
    main()
