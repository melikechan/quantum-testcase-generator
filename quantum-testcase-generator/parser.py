import json
import logging


class Parser:
    def __init__(self, input_file):
        self.input_file = input_file

    def parse_file(self) -> list:
        with open(self.input_file, 'r') as file:
            data = json.load(file)

            return data

    def parse_single_args(self, data: dict) -> dict:
        args = data['args']

        if data['dataType'] is None:
            data_type = 'int'
        elif data['dataType'] not in ['int', 'float', 'str']:
            logging.error(f'Invalid data type {data["dataType"]}:')
            raise Exception('Invalid data type')
        else:
            data_type = data['dataType']

        if data_type != 'str':
            lower_bound = args['valueLowerBound'] if 'valueLowerBound' in args else None
            upper_bound = args['valueUpperBound'] if 'valueUpperBound' in args else None

        return {
            'data_type': data_type,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound
        }

    def parse_array_args(self, data: dict) -> dict:
        args = data['args']

        if data['dataType'] is None:
            data_type = 'int'
        elif data['dataType'] not in ['int', 'float', 'str']:
            logging.error(f'Invalid data type {data["dataType"]}:')
            raise Exception('Invalid data type')
        else:
            data_type = data['dataType']

        if data_type != 'str':
            lower_bound = args['valueLowerBound'] if 'valueLowerBound' in args else None
            upper_bound = args['valueUpperBound'] if 'valueUpperBound' in args else None
            sum_elements = args['sumElements'] if 'sumElements' in args else None
            constraints = args['constraints'] if 'constraints' in args else None

        return {
            'data_type': data_type,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'sum_elements': sum_elements,
            'constraints': constraints
        }

    def parse_graph_args(self, data: dict) -> dict:
        args = data['args']

        weight_lower_bound = args['weightLowerBound'] if 'weightLowerBound' in args else None
        weight_upper_bound = args['weightUpperBound'] if 'weightUpperBound' in args else None

        is_directed = args['isDirected'] if 'isDirected' in args else False
        is_weighted = args['isWeighted'] if 'isWeighted' in args else False

        is_cyclic = True if 'cyclic' in args['constraints'] else False
        is_tree = True if 'tree' in args['constraints'] else False
        has_self_loops = True if 'self_loops' in args['constraints'] else False
        has_multi_edges = True if 'multi_edges' in args['constraints'] else False

        return {
            'weight_lower_bound': weight_lower_bound,
            'weight_upper_bound': weight_upper_bound,
            'is_directed': is_directed,
            'is_weighted': is_weighted,
            'is_cyclic': is_cyclic,
            'is_tree': is_tree,
            'has_self_loops': has_self_loops,
            'has_multi_edges': has_multi_edges
        }
