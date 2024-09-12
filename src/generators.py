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
    # TODO - Implement tree-bipartite etc. graph
    def __init__(self, n: int, m: int, weight: list[int], weight_sum: int, directed: bool):
        super().__init__()
        self.n = n
        self.m = m
        self.weight = weight  # [l, r]
        self.weight_sum = weight_sum
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

    def get_matrix(self) -> list:
        adj_matrix = [[0 for _ in range(self.n)] for _ in range(self.n)]

        current_sum = 0 if self.weight_sum == None else self.weight_sum
        for _ in range(self.m):
            u, v = self.rng.get_random_number(0, self.n - 1, 2)
            w = (
                self.rng.get_random_number(self.weight[0], self.weight[1])[0]
                if self.weight != None and len(self.weight) == 2
                else 1
            )
            adj_matrix[u][v] = w

            if current_sum != None:
                current_sum += w

            if not self.directed:
                adj_matrix[v][u] = w

        # Adjust the weights if needed
        if self.weight_sum != None:
            while current_sum != self.weight_sum:
                diff = self.weight_sum - current_sum

                u = self.rng.get_random_number(0, self.n - 1)[0]
                v = self.rng.get_random_number(0, self.n - 1)[0]

                if adj_matrix[u][v] == 0:
                    continue

                if diff > 0:
                    w = self.rng.get_random_number(
                        self.weight[0], self.weight[1])[0]

                    current_sum -= adj_matrix[u][v]

                    adj_matrix[u][v] = min(
                        diff, self.weight[1] - adj_matrix[u][v])

                    current_sum += adj_matrix[u][v]
                else:
                    w = self.rng.get_random_number(
                        self.weight[0], self.weight[1])[0]

                    current_sum -= adj_matrix[u][v]

                    adj_matrix[u][v] = max(
                        diff, self.weight[0] - adj_matrix[u][v])

                    current_sum += adj_matrix[u][v]

        return adj_matrix

    def get_adj_list(self) -> list:
        adj_list = [[] for _ in range(self.n)]

        current_sum = 0 if self.weight_sum != None else None
        for _ in range(self.m):
            u, v = self.rng.get_random_number(0, self.n - 1, 2)
            w = (
                self.rng.get_random_number(self.weight[0], self.weight[1])[0]
                if self.weight != None and len(self.weight) == 2
                else 1
            )
            adj_list[u].append((v, w))

            if current_sum != None:
                current_sum += w

            if not self.directed:
                adj_list[v].append((u, w))

        # Adjust the weights if needed
        if self.weight_sum != None:
            while current_sum != self.weight_sum:
                diff = self.weight_sum - current_sum

                u = self.rng.get_random_number(0, self.n - 1)[0]
                if adj_list[u] == []:
                    continue

                v = self.rng.get_random_number(0, len(adj_list[u]) - 1)[0]

                if diff > 0:
                    w = self.rng.get_random_number(
                        self.weight[0], self.weight[1])[0]

                    current_sum -= adj_list[u][v][1]

                    adj_list[u][v] = (adj_list[u][v][0], min(
                        diff, self.weight[1] - adj_list[u][v][1]))

                    current_sum += adj_list[u][v][1]
                else:
                    w = self.rng.get_random_number(
                        self.weight[0], self.weight[1])[0]

                    current_sum -= adj_list[u][v][1]

                    adj_list[u][v] = (adj_list[u][v][0], max(
                        diff, self.weight[0] - adj_list[u][v][1]))

                    current_sum += adj_list[u][v][1]

        return adj_list

    def get_edge_list(self) -> list:
        edge_list = []

        current_sum = 0 if self.weight_sum != None else None
        for _ in range(self.m):
            u, v = self.rng.get_random_number(0, self.n - 1, 2)
            w = (
                self.rng.get_random_number(self.weight[0], self.weight[1])[0]
                if self.weight != None and len(self.weight) == 2
                else 1
            )
            edge_list.append((u, v, w))

            if current_sum != None:
                current_sum += w

            if not self.directed:
                edge_list.append((v, u, w))

        # Adjust the weights if needed
        if self.weight_sum != None:
            while current_sum != self.weight_sum:
                diff = self.weight_sum - current_sum
                edge_number = self.rng.get_random_number(0, self.m - 1)[0]
                if diff > 0:
                    w = self.rng.get_random_number(
                        self.weight[0], self.weight[1])[0]

                    current_sum -= edge_list[edge_number][2]

                    edge_list[edge_number][2] = min(
                        diff, self.weight[1] - edge_list[edge_number][2])

                    current_sum += edge_list[edge_number][2]
                else:
                    w = self.rng.get_random_number(
                        self.weight[0], self.weight[1])[0]

                    current_sum -= edge_list[edge_number][2]

                    edge_list[edge_number][2] = max(
                        diff, self.weight[0] - edge_list[edge_number][2])

                    current_sum += edge_list[edge_number][2]

        return edge_list


class StringGenerator:
    # TODO
    pass
