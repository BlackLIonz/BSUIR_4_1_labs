import numpy as np


class ResourceAllocation:
    def __init__(self, f_table):
        self.f_table = f_table
        self.n, self.c = self.f_table.shape
        self.c = self.c - 1
        self.B = [[] for i in range(self.n)]
        self.B[0] = list(self.f_table[0, :])
        self.x = {}
        self.plan = []

    def _get_B_k(self, k, y):
        b = [self.f_table[k, z] + self.B[k - 1][y - z] for z in range(y + 1)]
        indices = [i for i, x in enumerate(b) if x == max(b)]
        self.x[(k, y)] = indices
        return max(b)

    def _get_B(self):
        for k in range(1, self.n):
            self.B[k].append(0)
            for y in range(1, self.c + 1):
                self.B[k].append(self._get_B_k(k, y))

    def _get_max_value(self):
        max = self.B[0][0]
        max_index = (0, 0)
        for i, row in enumerate(self.B):
            for j, value in enumerate(row):
                if max < value:
                    max = value
                    max_index = (i, j)
        return max, max_index

    def _get_plan(self, max_indexes):
        index = max_indexes[1]
        resurses = self.c
        for process_number in range(self.n - 1, -1, -1):
            if process_number == 0:
                self.plan.append(resurses)
                return
            x = self.x.get((process_number, index), (0,))[0]
            resurses -= x
            self.plan.append(x)
            index = resurses

    def solve(self):
        self._get_B()
        max_value, max_indexes = self._get_max_value()
        self._get_plan(max_indexes)
        return self.plan[::-1], self.B


# if __name__ == '__main__':
#     table = np.array([[0, 3, 4, 5, 8, 9, 10],
#                       [0, 2, 3, 7, 9, 12, 13],
#                       [0, 1, 2, 6, 11, 11, 13]])
#     task = ResourceAllocation(table)
#     plan, _ = task.solve()
#     print(plan)
