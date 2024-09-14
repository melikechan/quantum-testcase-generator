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

        result = self.rng.get_random_number(self.l, self.r, self.num_numbers)
        current_sum = sum(result)

        # Adjust the numbers if needed
        while current_sum != self.sum:
            diff = self.sum - current_sum
            if diff > 0:
                index = self.rng.get_random_number(0, self.num_numbers - 1)[0]
                result[index] += min(diff, self.r - result[index])
            else:
                index = self.rng.get_random_number(0, self.num_numbers - 1)[0]
                result[index] += max(diff, self.l - result[index])
                current_sum = sum(result)
        print(sum(result), self.sum)


class GraphGenerator(BaseGenerator):
    def __init__(self, n: int, m: int, weight: list[int], weight_sum: int = None,
                 directed: bool = False, cyclic: bool = False,
                 self_loops: bool = False, multi_edges: bool = False,
                 tree: bool = False):
        super().__init__()
        self.n = n
        self.m = m
        self.weight = weight  # [l, r]

        self.weighted = weight != None
        self.weight_sum = weight_sum

        self._directed = False

        self._cyclic = False
        self._self_loops = False
        self._multi_edges = False
        self._tree = False

        self.directed = directed
        self.cyclic = cyclic
        self.self_loops = self_loops
        self.multi_edges = multi_edges
        self.tree = tree

        self.graph = {{} for _ in range(n)}

    @property
    def tree(self) -> bool:
        return self._tree

    @tree.setter
    def tree(self, value: bool):
        self._tree = value

        if value:
            self._cyclic = False
            self._multi_edges = False

            self.m = self.n - 1

    @property
    def cyclic(self) -> bool:
        return self._cyclic

    @cyclic.setter
    def cyclic(self, value: bool):
        self._cyclic = value

        if value:
            self._tree = False
        else:
            self._self_loops = False
            self._directed = True

    def check_cycle(self) -> bool:
        visited = [False] * self.n
        stack = []

        stack.append(0)
        visited[0] = True

        while stack:
            u = stack.pop()

            for v in self.graph[u]:
                if not visited[v]:
                    stack.append(v)
                    visited[v] = True
                else:
                    return True

    def build_graph(self):
        current_sum = None if self.weight_sum == None else 0

        for _ in range(self.m):
            u, v = self.rng.get_random_number(0, self.n - 1, 2)
            w = (
                self.rng.get_random_number(self.weight[0], self.weight[1])[0]
                if self.weight != None and len(self.weight) == 2
                else 1
            )

            if not self.multi_edges and v in self.graph[u]:
                continue

            self.graph[u][v] = w

            if current_sum != None:
                current_sum += w

            if not self.directed:
                self.graph[v][u] = w

        # TODO: Check graph in a more optimized way
        if not self._cyclic:
            if self.check_cycle():
                self.build_graph()

        if self.weight_sum != None:
            while current_sum != self.weight_sum:
                diff = self.weight_sum - current_sum

                u = self.rng.get_random_number(0, self.n - 1)[0]
                v = self.rng.get_random_number(0, self.n - 1)[0]

                if not self.multi_edges and v in self.graph[u]:
                    continue

                if diff > 0:
                    w = self.rng.get_random_number(
                        self.weight[0], self.weight[1])[0]

                    current_sum -= self.graph[u][v]

                    self.graph[u][v] = min(
                        diff, self.weight[1] - self.graph[u][v])

                    current_sum += self.graph[u][v]
                else:
                    w = self.rng.get_random_number(
                        self.weight[0], self.weight[1])[0]

                    current_sum -= self.graph[u][v]

                    self.graph[u][v] = max(
                        diff, self.weight[0] - self.graph[u][v])

                    current_sum += self.graph[u][v]

    def get_graph(self, mode: str) -> list:
        if mode == "adj_matrix":
            return self.get_matrix()
        elif mode == "adj_list":
            return self.get_adj_list()
        elif mode == "edge_list":
            return self.get_edge_list()
        else:
            raise Exception("Invalid mode")

    def get_matrix(self) -> list:
        if self.multi_edges:
            raise Exception("Cannot generate matrix for multi-edges")

        if not self.weighted:
            adj_matrix = [[0] * self.n for _ in range(self.n)]

            for u in range(self.n):
                for v in self.graph[u]:
                    adj_matrix[u][v] = 1
        else:
            adj_matrix = [[0] * self.n for _ in range(self.n)]

            for u in range(self.n):
                for v in self.graph[u]:
                    adj_matrix[u][v] = self.graph[u][v]

        return adj_matrix

    def get_adj_list(self) -> list:
        adj_list = [[] for _ in range(self.n)]

        for u in range(self.n):
            for v in self.graph[u]:
                if not self.weighted:
                    adj_list[u].append(v)
                else:
                    adj_list[u].append((v, self.graph[u][v]))

        return adj_list

    def get_edge_list(self) -> list:
        edge_list = []

        for u in range(self.n):
            for v in self.graph[u]:
                if not self.weighted:
                    edge_list.append((u, v))
                else:
                    edge_list.append((u, v, self.graph[u][v]))

        return edge_list

class StringGenerator:
    # TODO
    pass
