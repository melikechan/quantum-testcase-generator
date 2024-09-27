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
    data = input_parser.parse_file()

    for i in range(test_case_count):
        logging.info(f'Generating testcase {i+1}...')

        single_number_generator = generators.SingleNumberGenerator(
            l=-10**9, r=10**9)
        array_generator = generators.ArrayGenerator(
            l=-10**9, r=10**9)
        graph_generator = generators.GraphGenerator(node_count=0, edge_count=0)

        variables = {}
        outputfile_path = os.path.join(outputdir, f'testcase_{i+1}.txt')

        with open(outputfile_path, 'w') as outputfile:
            for d in data:
                if d['inputType'] == 'single':
                    generator_attributes = input_parser.parse_single_args(d)
                    data_type = generator_attributes['data_type']

                    if data_type == 'int' or data_type == 'float':
                        lower_bound = generator_attributes['lower_bound']
                        upper_bound = generator_attributes['upper_bound']

                        lower_bound = variables[lower_bound] if lower_bound in variables else lower_bound
                        upper_bound = variables[upper_bound] if upper_bound in variables else upper_bound

                        single_number_generator.l = lower_bound
                        single_number_generator.r = upper_bound
                        variables[d['variableName']
                                  ] = single_number_generator.get_number()
                    else:
                        # String generator not implemented yet
                        raise NotImplementedError(
                            'String generator is not implemented yet')

                    outputfile.write(str(variables[d['variableName']]) + ' ')
                elif d['inputType'] == 'array':
                    generator_attributes = input_parser.parse_array_args(d)
                    data_type = generator_attributes['data_type']
                    
                    dimensions = d['dimensions']

                    # Replace variables
                    for i in range(len(dimensions)):
                        if dimensions[i] in variables:
                            dimensions[i] = variables[dimensions[i]]

                    if data_type == 'int' or data_type == 'float':
                        lower_bound = generator_attributes['lower_bound']
                        upper_bound = generator_attributes['upper_bound']
                        sum_elements = generator_attributes['sum_elements']

                        lower_bound = variables[lower_bound] if lower_bound in variables else lower_bound
                        upper_bound = variables[upper_bound] if upper_bound in variables else upper_bound
                        sum_elements = variables[sum_elements] if sum_elements in variables else sum_elements

                        array_generator.l = lower_bound
                        array_generator.r = upper_bound
                        array_generator.dimensions = dimensions
                        array_generator.sum = sum_elements

                        variables[d['variableName']
                                  ] = array_generator.get_array()
                    else:
                        # String generator not implemented yet
                        raise NotImplementedError(
                            'String generator is not implemented yet')

                    for row in range(len(variables[d['variableName']])):
                        outputfile.write(' '.join(
                            map(str, variables[d['variableName']][row])))

                        if row != len(variables[d['variableName']]) - 1:
                            outputfile.write('\n')

                elif d['inputType'] == 'graph':
                    generator_attributes = input_parser.parse_graph_args(d)

                    node_count = variables[d['nodeCount']
                                           ] if d['nodeCount'] in variables else d['nodeCount']
                    edge_count = variables[d['edgeCount']
                                           ] if d['edgeCount'] in variables else d['edgeCount']

                    output_mode = d['outputMode']

                    if output_mode not in ['adjacency_matrix', 'edge_list']:
                        logging.error(f'Invalid output mode {output_mode}')
                        raise Exception('Invalid output mode')

                    graph_generator.node_count = node_count
                    graph_generator.edge_count = edge_count

                    graph_generator.directed = generator_attributes['is_directed']
                    graph_generator.weighted = generator_attributes['is_weighted']
                    graph_generator.self_loops = generator_attributes['has_self_loops']
                    graph_generator.multi_edges = generator_attributes['has_multi_edges']
                    graph_generator.cyclic = generator_attributes['is_cyclic']
                    graph_generator.tree = generator_attributes['is_tree']

                    weight_lower_bound = variables[generator_attributes['weight_lower_bound']
                                                   ] if generator_attributes['weight_lower_bound'] in variables else generator_attributes['weight_lower_bound']
                    weight_upper_bound = variables[generator_attributes['weight_upper_bound']
                                                   ] if generator_attributes['weight_upper_bound'] in variables else generator_attributes['weight_upper_bound']

                    graph_generator.weight = [
                        weight_lower_bound, weight_upper_bound]

                    graph_generator.build_graph()
                    graph = graph_generator.get_graph(mode=output_mode)
                    variables[d['variableName']] = graph

                    if output_mode == 'adj_matrix':
                        for row in range(len(graph)):
                            outputfile.write(' '.join(
                                map(str, graph[row])))

                            if row != len(graph) - 1:
                                outputfile.write('\n')
                    elif output_mode == 'edge_list':
                        for edge in graph:
                            outputfile.write(f'{edge[0]} {edge[1]}')

                            if graph_generator.weighted:
                                outputfile.write(f' {edge[2]}')

                            outputfile.write('\n')
                    else:
                        logging.error(f'Invalid output mode {output_mode}')
                        raise Exception('Invalid output mode')
                else:
                    logging.error(f'Invalid type {d["inputType"]}')
                    raise Exception('Invalid type')

                if d['skipToNextLine']:
                    outputfile.write('\n')
        logging.info(f'Testcase {i+1} generated: {outputfile_path}')


if __name__ == '__main__':
    main()
