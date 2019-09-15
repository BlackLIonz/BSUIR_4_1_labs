import math

import numpy as np

from SAIO.lab1.dual_simplex_method import DualSimplexMethod


class BranchBorderMethod:
    def __init__(self, A, c, b, d_down_asterisk, d_up_asterisk):
        self.A = A
        self.c = c
        self.b = b
        self.d_down_asterisk = d_down_asterisk
        self.d_up_asterisk = d_up_asterisk
        self.task_list = []
        self.r = -np.Inf
        self.solve_x = None

    @staticmethod
    def get_non_integer(values):
        for i, value in enumerate(values):
            if math.floor(value) != value:
                return i
        return None

    def solve(self):
        self.task_list.append(DualSimplexMethod(self.A, self.c, self.b,
                                                self.d_down_asterisk, self.d_up_asterisk))
        while self.task_list:
            task = self.task_list.pop(0)
            try:
                x0, r = task.solve()
            except TypeError:
                continue

            non_int = self.get_non_integer(x0)
            if non_int is None:
                if r > self.r:
                    self.solve_x = x0
                    self.r = r
                continue
            l = np.floor(x0[non_int])
            new_d_down, new_d_up = np.copy(task.d_down_asterisk), np.copy(task.d_up_asterisk)
            new_d_down[non_int] = l + 1
            new_d_up[non_int] = l
            self.task_list.append(DualSimplexMethod(self.A, self.c, self.b,
                                                    new_d_down, task.d_up_asterisk))
            self.task_list.append(DualSimplexMethod(self.A, self.c, self.b,
                                                    task.d_down_asterisk, new_d_up))

        if self.solve_x:
            return self.solve_x

# if __name__ == '__main__':
#    A = np.array([[1, -5, 3, 1, 0, 0],
#                  [4, -1, 1, 0, 1, 0],
#                  [2, 4, 2, 0, 0, 1]])
#    b = np.array([-8, 22, 30])
#    c = np.array([7, -2, 6, 0, 5, 2])
#    d_down = np.array([2, 1, 0, 0, 1, 1])
#    d_up = np.array([6, 6, 5, 2, 4, 6])
#    bb = BranchBorderMethod(A, c, b, d_down, d_up)
#    x = bb.solve()
#    print(f'x = {str(x)}')
