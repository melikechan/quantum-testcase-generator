import rng_utils

# Numeric Values
class BaseGenerator:
    def __init__(self):
        self.rng = rng_utils.RandomNumberGenerator()


class SingleNumberGenerator(BaseGenerator):
    def __init__(self, l: int, r: int):
        super().__init__()
        self.l = l
        self.r = r

    def get_random_number(self) -> int:
        return self.rng.get_random_number(self.l, self.r)[0]


class TupleGenerator(BaseGenerator):
    def __init__(self, l: int, r: int, num_numbers: int):
        super().__init__()
        self.l = l
        self.r = r
        self.num_numbers = num_numbers

    def get_random_numbers(self) -> list:
        return self.rng.get_random_number(self.l, self.r, self.num_numbers)


class ArrayGenerator(BaseGenerator):
    # TODO
    pass

class GraphGenerator(BaseGenerator):
    # TODO
    pass

class StringGenerator:
    # TODO
    pass