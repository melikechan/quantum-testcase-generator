import json

class Parser:
    def __init__(self, input_file):
        self.input_file = input_file

    def parse(self) -> list:
        with open(self.input_file, 'r') as file:
            data = json.load(file)

        return data