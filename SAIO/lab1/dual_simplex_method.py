import sys
import numpy as np
from collections import OrderedDict

# sys.stdout = open("logger.txt", "w+")


class DualSimplexMethod:

    def __init__(self, A, c, b, d_down_asterisk, d_up_asterisk, J_basis=None):
        self.A = A
        self.c = c
        self.b = b
        self.d_down_asterisk = d_down_asterisk
        self.d_up_asterisk = d_up_asterisk

        self.m, self.n = self.A.shape

        self.J = list(range(0, self.n))
        self.J_basis = self.J[-self.m:] if J_basis is None else J_basis
        self.A_basis = self.get_A_basis()
        self.B = np.linalg.inv(self.A_basis)
        self.c_basis = self.get_c_basis()
        # print('====================Init=================================')
        # print(f'A = \n {str(self.A)}')
        # print(f'B = \n {str(self.B)}')
        # print(f'c = {str(self.c)}')
        # print(f'b = {str(self.b)}')
        # print(f'd_down = {str(self.d_down_asterisk)}')
        # print(f'd_up = {str(self.d_up_asterisk)}')
        # print('================End Init=================================')

        self.delta_rate = np.zeros(self.n)
        self.J_non_basis = None
        self.J_non_basis_plus = None
        self.J_non_basis_minus = None
        self.xi = None
        self.u = None
        self.invalid_j = None
        self.sigma = None
        self.delta_y = None
        self.j_asterisk = None

    def get_y_hatch(self):
        self.c_basis = self.get_c_basis()
        return self.c_basis.dot(self.B)

    def get_delta_rate(self):
        delta_rate = []
        for j in range(self.n):
            mul = round(self.A[:, j].dot(self.get_y_hatch()), 6)
            delta_rate.append(np.subtract(mul, self.c[j]))
        self.delta_rate = delta_rate
        return self.delta_rate

    def get_new_rate(self):
        for i in range(self.n):
            self.delta_rate[i] += self.sigma[-1] * self.u[i]
        return self.delta_rate

    def get_c_basis(self):
        basis = np.ones(self.m)
        for i in range(self.m):
            k = self.J_basis[i]
            basis[i] = self.c[k]
        return basis

    def get_A_basis(self):
        while True:
            basis = np.ones((self.m, self.m))
            for i in range(self.m):
                k = int(self.J_basis[i])
                basis[:, i] = self.A[:, k]
            self.A_basis = basis
            if np.linalg.det(self.A_basis) != 0:
                break
        return basis

    def get_J_non_basis(self):
        J_non_basis = []
        for i in range(len(self.J)):
            if not self.J[i] in self.J_basis:
                J_non_basis.append(self.J[i])
        J_non_basis_plus = []
        J_non_basis_minus = []
        for j in J_non_basis:
            if self.delta_rate[j] >= 0:
                J_non_basis_plus.append(j)
            else:
                J_non_basis_minus.append(j)
        self.J_non_basis, self.J_non_basis_plus, self.J_non_basis_minus = \
            J_non_basis, J_non_basis_plus, J_non_basis_minus
        return J_non_basis, J_non_basis_plus, J_non_basis_minus

    def get_xi(self):
        xi = {}
        for j in self.J_non_basis:
            if j in self.J_non_basis_minus:
                xi[j] = self.d_up_asterisk[j]
            elif j in self.J_non_basis_plus:
                xi[j] = self.d_down_asterisk[j]
        basis_xi = self.get_basis_xi(xi)
        for i in range(len(self.J_basis)):
            xi[self.J_basis[i]] = basis_xi[i]
        sort_xi = OrderedDict(sorted(xi.items()))
        self.xi = list(map(lambda x: round(x, 4), sort_xi.values()))
        return self.xi

    def get_basis_xi(self, non_basis_xi):
        sigma = 0
        for j in self.J_non_basis:
            sigma = np.add(sigma, np.dot(self.A[:, j], non_basis_xi[j]))
        return self.B.dot(np.subtract(self.b, sigma))

    def get_invalid_j_basis(self):
        for index, j in enumerate(self.J_basis):
            j = int(j)
            if self.xi[j] < self.d_down_asterisk[j] or self.xi[j] > self.d_up_asterisk[j]:
                self.invalid_j = index, j
                return self.invalid_j
        return None

    def get_delta_y(self):
        index, j = self.invalid_j
        e_index = np.zeros(self.m)
        e_index[index] = 1
        u_j = 1 if self.xi[j] < self.d_down_asterisk[j] else -1
        self.delta_y = u_j * e_index.dot(self.B)
        return self.delta_y

    def get_all_u(self):
        u = {}
        for i in range(self.n):
            u[i] = self.delta_y.dot(self.A[:, i])
        self.u = list(u.values())
        return self.u

    def get_sigmas(self):
        sigma = {}
        for j in self.J_non_basis:
            if (j in self.J_non_basis_plus and self.u[j] < 0) or (j in self.J_non_basis_minus and self.u[j] > 0):
                sigma[j] = -self.delta_rate[j] / self.u[j]
            else:
                sigma[j] = np.Inf
        self.sigma = sigma
        return sigma

    def is_sigma_less_than_inf(self):
        sigma = self.get_min_sigma()
        for index, value in self.sigma.items():  # for name, age in dictionary.iteritems():  (for Python 2.x)
            if value == sigma:
                self.j_asterisk = index
                break
        self.sigma[-1] = sigma
        if self.sigma[-1] < np.Inf:
            return True
        else:
            return False

    def get_min_sigma(self):
        sigma_zero = np.inf
        for index, sigma in self.sigma.items():
            if sigma == np.inf:
                continue
            if sigma < sigma_zero:
                sigma_zero = sigma
        return sigma_zero

    def get_new_J_basis(self):
        self.J_basis[self.invalid_j[0]] = self.j_asterisk
        return self.get_J_non_basis()

    def get_B(self):
        self.B = np.linalg.inv(self.A_basis)

    def solve(self):
        self.get_y_hatch()
        # print(f'y_hatch = {str(self.get_y_hatch())}')
        self.get_delta_rate()
        # print(f'delta_rate = {str(self.delta_rate)}')
        self.get_J_non_basis()
        # print(f'J_basis = {str(self.J_basis)}\n'
        #       f'J_non_basis_minus = {str(self.J_non_basis_minus)}\n'
        #       f'J_non_basis_plus = {str(self.J_non_basis_plus)}')
        while True:
            # print('====================Next iteration=======================')
            self.get_xi()
            # print(f'xi = {str(self.xi)}')
            if not self.get_invalid_j_basis():
                xi = [round(x, 4) for x in self.xi]
                value = round(self.c.dot(self.xi), 4)
                return xi, value
            # print(f'jk = {self.invalid_j[0]}, where k = {self.invalid_j[1]}')
            self.get_delta_y()
            # print(f'delta_y = {str(self.delta_y)}')
            self.get_all_u()
            # print(f'u = {str(self.u)}')
            self.get_sigmas()
            if not self.is_sigma_less_than_inf():
                return None
            # print(f'sigma_0 = {str(self.sigma[-1])}')
            self.get_new_rate()
            # print(f'new rate = {str(self.delta_rate)}')
            self.get_new_J_basis()
            # print(f'J_basis = {str(self.J_basis)}\n'
            #       f'J_non_basis_minus = {str(self.J_non_basis_minus)}\n'
            #       f'J_non_basis_plus = {str(self.J_non_basis_plus)}')
            self.get_A_basis()
            # print(f'A_basis = \n{str(self.A_basis)}')
            self.get_B()
            # print(f'B = \n{str(self.B)}')


def main():
    A = np.array([[2, 1, 0, 3, -1, -1],
                  [0, 1, -2, 1, 0, 3],
                  [3, 0, 1, 1, 1, 1]],)
    c = np.array([0, -1, 1, 0, 4, 3])
    b = np.array([2, 2, 5])
    d_down_asterisk = [2, 0, -1, -3, 2, 1]
    d_up_asterisk = [7, 3, 2, 3, 4, 5]
    ds = DualSimplexMethod(A, c, b, d_down_asterisk, d_up_asterisk, [0, 1, 2])
    result = ds.solve()
    # print('====================Result==============================')
    # print(f'Result = {result}')


if __name__ == '__main__':
    main()
