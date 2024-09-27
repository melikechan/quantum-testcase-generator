import rng_utils
import random


class BaseGenerator:
    """
    Base class for all numeric generators, including a random number generator.
    """

    def __init__(self):
        self.rng = rng_utils.RandomNumberGenerator()


class SingleNumberGenerator(BaseGenerator):
    """
    Class for generating a single number within a given range.

    Args:
        l (int): Lower bound of the range.
        r (int): Upper bound of the range.
    """

    def __init__(self, l: int, r: int):
        super().__init__()
        self.l = l
        self.r = r

    """
    Get a single random number within the given range [l, r].

    Returns:
        int: Random number within the given range [l, r].
    """

    def get_number(self) -> int:
        return self.rng.get_random_number(self.l, self.r)[0]


class ArrayGenerator(BaseGenerator):
    """
    Class for generating an array of random numbers within a given range.

    Args:
        l (int): Lower bound of the range.
        r (int): Upper bound of the range.
    """

    def __init__(self, l: int, r: int):
        super().__init__()
        self.l = l
        self.r = r

    @property
    def dimensions(self) -> list[int]:
        return self._dimensions

    @dimensions.setter
    def dimensions(self, value: list[int]):
        self._dimensions = value

        self.num_numbers = 1
        for dimension in value:
            self.num_numbers *= dimension

    @property
    def sum(self) -> int:
        return self._sum

    @sum.setter
    def sum(self, value: int):
        self._sum = value

        if value is not None and (value < self.l * self.num_numbers or value > self.r * self.num_numbers):
            raise Exception("Invalid sum")

    """
    Get an array of random numbers within the given range [l, r].

    Returns:
        list: Array of random numbers within the given range [l, r].
    """

    def get_array(self) -> list:
        result = []

        result = self.rng.get_random_number(self.l, self.r, self.num_numbers)
        not_used_indices = set(range(self.num_numbers))

        # Adjust the numbers if needed
        if self.sum is not None:
            current_sum = sum(result)
            while current_sum != self.sum:
                diff = self.sum - current_sum
                index = random.choice(list(not_used_indices))

                not_used_indices.remove(index)

                previous_val = result[index]

                if diff > 0:
                    result[index] += min(diff, self.r - result[index])
                else:
                    result[index] += max(diff, self.l - result[index])

                current_sum += result[index] - previous_val

        # Reshape the array
        for dimension in reversed(self.dimensions):
            result = [
                result[i:i + dimension] for i in range(0, len(result), dimension)]

        result = result[0] if len(result) == 1 else result
        return result


class GraphGenerator(BaseGenerator):
    def __init__(self, node_count: int, edge_count: int, weight: list[int] = None, weight_sum: int = None):
        super().__init__()

        self._node_count = node_count
        self._edge_count = edge_count

        self.weight = weight  # [l, r]

        self.weighted = weight != None
        self.weight_sum = weight_sum

        self._directed = False

        self._cyclic = False
        self._self_loops = False
        self._multi_edges = False
        self._tree = False

        self.graph = [{} for _ in range(node_count)]

    @property
    def tree(self) -> bool:
        return self._tree

    @tree.setter
    def tree(self, value: bool):
        self._tree = value

        if value:
            self._cyclic = False
            self._multi_edges = False

            self.edge_count = self.node_count - 1

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

    @property
    def self_loops(self) -> bool:
        return self._self_loops

    @self_loops.setter
    def self_loops(self, value: bool):
        self._self_loops = value

        if value:
            self._cyclic = True

    @property
    def multi_edges(self) -> bool:
        return self._multi_edges

    @multi_edges.setter
    def multi_edges(self, value: bool):
        self._multi_edges = value

        if value:
            self._cyclic = True

    @property
    def directed(self) -> bool:
        return self._directed

    @directed.setter
    def directed(self, value: bool):
        self._directed = value

    @property
    def weight_sum(self) -> int:
        return self._weight_sum

    @property
    def node_count(self) -> int:
        return self._node_count

    @node_count.setter
    def node_count(self, value: int):
        self._node_count = value

        # Arrange the graph
        if value < len(self.graph):
            self.graph = self.graph[:value]
        elif value > len(self.graph):
            self.graph += [{} for _ in range(value - len(self.graph))]

    @property
    def edge_count(self) -> int:
        return self._edge_count

    @edge_count.setter
    def edge_count(self, value: int):
        self._edge_count = value

    @weight_sum.setter
    def weight_sum(self, value: int):
        self._weight_sum = value

        if value is not None and (value < self.l * self.edge_count or value > self.r * self.edge_count):
            raise Exception("Invalid weight sum")

    def check_cycle(self) -> bool:
        visited = [False] * self.node_count
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

        for _ in range(self.edge_count):
            u, v = self.rng.get_random_number(0, self.node_count - 1, 2)
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

                u = self.rng.get_random_number(0, self.node_count - 1)[0]
                v = self.rng.get_random_number(0, self.node_count - 1)[0]

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
        elif mode == "edge_list":
            return self.get_edge_list()
        else:
            raise Exception("Invalid mode")

    def get_matrix(self) -> list:
        if self.multi_edges:
            raise Exception("Cannot generate matrix for multi-edges")

        if not self.weighted:
            adj_matrix = [
                [0] * self.node_count for _ in range(self.node_count)]

            for u in range(self.node_count):
                for v in self.graph[u]:
                    adj_matrix[u][v] = 1
        else:
            adj_matrix = [
                [0] * self.node_count for _ in range(self.node_count)]

            for u in range(self.node_count):
                for v in self.graph[u]:
                    adj_matrix[u][v] = self.graph[u][v]

        return adj_matrix

    def get_edge_list(self) -> list:
        edge_list = []

        for u in range(self.node_count):
            for v in self.graph[u]:
                if not self.weighted:
                    edge_list.append((u, v))
                else:
                    edge_list.append((u, v, self.graph[u][v]))

        return edge_list


class StringGenerator:
    # TODO
    pass
