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

    def get_number(self) -> int:
        return self.rng.get_random_number(self.l, self.r)[0]


class TupleGenerator(BaseGenerator):
    def __init__(self, l: int, r: int, num_numbers: int):
        super().__init__()
        self.l = l
        self.r = r
        self.num_numbers = num_numbers

    def get_tuple(self) -> list:
        return self.rng.get_random_number(self.l, self.r, self.num_numbers)


class ArrayGenerator(BaseGenerator):
    # TODO
    def __init__(self, l: int, r: int, num_numbers: int, sum_array: int):
        super().__init__()
        self.l = l
        self.r = r
        self.num_numbers = num_numbers
        self.sum = sum_array
        if self.sum < l * num_numbers or self.sum > r * num_numbers:
            raise Exception("Invalid sum")

    def get_array(self) -> list:
        result = []

        # Well, I guess this is a very inefficient way to generate an array with a specific sum.
        while sum(result) != self.sum:
            result = self.rng.get_random_number(self.l, self.r, self.num_numbers)


class GraphGenerator(BaseGenerator):
    # TODO
    def __init__(self, n: int, m: int, weight: [int, int], directed: bool):
        super().__init__()
        self.n = n
        self.m = m
        self.weight = weight
        self.directed = directed

    def get_graph(self, mode: str) -> list:
        if mode == "adj_matrix":
            return self.get_matrix()
        elif mode == "adj_list":
            return self.get_adj_list()
        elif mode == "edge_list":
            return self.get_edge_list()
        else:
            raise Exception("Invalid mode")

    def get_matrix(self, weighted: bool) -> list:
        adj_matrix = [[0 for _ in range(self.n)] for _ in range(self.n)]

        for _ in range(self.m):
            u, v = self.rng.get_random_number(0, self.n - 1, 2)
            w = (
                self.rng.get_random_number(self.weight[0], self.weight[1])[0]
                if self.weight != None
                else 1
            )
            adj_matrix[u][v] = w

            if not self.directed:
                adj_matrix[v][u] = w


class StringGenerator:
    # TODO
    pass
