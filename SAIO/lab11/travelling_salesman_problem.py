import copy

import numpy as np

from SAIO.lab10.assignment_problem import HungarianAlgorithm


class TravellingSalesmanProblem:
    def __init__(self, matrix):
        self.matrix = matrix
        self.r = np.inf
        self.plan = None

    def solve(self):
        tasks = [HungarianAlgorithm(copy.deepcopy(self.matrix))]
        while tasks:
            task = tasks.pop(0)
            plan = task.solve()
            circuit = self.get_circuit(plan)
            if circuit:
                min_circuit = min(self.get_circuit(plan)) if circuit else circuit[0]
            else:
                raise ValueError('min_circuit is empty')
            if len(min_circuit) == len(plan) and min_circuit[0][0] == min_circuit[-1][1]:
                rating = self.estimate_plan(plan)
                if rating < self.r:
                    self.r = rating
                    self.plan = min_circuit
                continue
            for curve in min_circuit:
                c = copy.deepcopy(task.matrix)
                i, j = curve
                c[i - 1, j - 1] = np.inf
                tasks.append(HungarianAlgorithm(c))
        return self.plan, self.r

    def estimate_plan(self, plan):
        rating = 0
        for i, j in plan:
            rating += self.matrix[i - 1, j - 1]
        return rating

    @staticmethod
    def get_circuit(plan):
        paths = []
        for i in range(len(plan)):
            path = [plan[i]]
            for j in range(i, len(plan)):
                curve = [(i, j) for i, j in plan if path[-1][1] == i]
                if len(curve) and curve[0] not in path:
                    path += curve
                else:
                    break
            if path[0][0] == path[-1][1]:
                if len(path) == len(plan):
                    return [path]
                paths.append(path)
        return paths


if __name__ == '__main__':
    matrix = np.array([[np.inf, 2, 1, 10, 6],
                       [4, np.inf, 3, 1, 3],
                       [2, 5, np.inf, 8, 4],
                       [6, 7, 13, np.inf, 3],
                       [10, 2, 4, 6, np.inf]])
    problem = TravellingSalesmanProblem(matrix)
    plan, r = problem.solve()
    path = [str(i) for i, j in plan] + [str(plan[-1][-1])]
    print('Path: ' + ' -> '.join(path))
    print(f'Cost: {r}')
