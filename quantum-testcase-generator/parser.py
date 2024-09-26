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

        dimensions = args['dimensions']

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
            'dimensions': dimensions,
            'lower_bound': lower_bound,
            'upper_bound': upper_bound,
            'sum_elements': sum_elements,
            'constraints': constraints
        }
