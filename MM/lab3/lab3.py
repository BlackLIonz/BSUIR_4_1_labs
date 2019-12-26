import math

import numpy as np
import matplotlib.pyplot as plt
from sympy import DiracDelta


class Processes:
    def __init__(self, h, K):
        self.h = h
        self.K = K

    @staticmethod
    def white_noise(n):
        return np.random.standard_normal(size=n)

    def process_realization(self, n, time=20, alpha=1, sigma=1, D=1):
        tau = time / n
        white_noise_sample = Processes.white_noise(n)
        time_steps = np.arange(0, time, tau)
        sample = [
            sum([
                self.h(D, alpha, sigma, tau * i) * white_noise_sample[j - i]
                for i in range(1, j + 1)
            ])
            for j in range(n)
        ]
        return sample, time_steps

    def mean(self, sample):
        return np.mean(sample)

    def var(self, sample):
        return np.var(sample)

    def solve(self):
        noise = Processes.white_noise(1000)
        plt.scatter(range(len(noise)), noise)
        plt.show()
        y, x = self.process_realization(1000)
        plt.plot(x, y)
        plt.show()
        mean = self.mean(y)
        var = self.var(y)
        print(f'Mean: {mean}')
        print(f'Var: {var}')
        # print(f'Dickey Fuller test: {self.dickey_fuller_test(y, len(x))}')
        # print(f'Slutsky test: {self.Slutsky_test()}')

    def dickey_fuller_test(self, realisation, n):
        X = realisation[:-1]
        Y = [realisation[i + 1] - realisation[i] for i in range(n - 1)]

        n_sum_xy = (n - 1) * sum([X[i] * Y[i] for i in range(n - 1)])
        x_sum_mul_y_sum = sum(X) * sum(Y)
        n_sum_x2 = (n - 1) * sum([x ** 2 for x in X])
        sum_x2 = sum(X) ** 2
        b = (n_sum_xy - x_sum_mul_y_sum) / (n_sum_x2 - sum_x2)
        return b

    def simpson(self, f, a, b, n):
        h = (b - a) / n
        s = f(a) + f(b)

        for i in np.arange(1, n, 2):
            s += 4 * f(a + i * h)
        for i in np.arange(2, n - 1, 2):
            s += 2 * f(a + i * h)

        return s * h / 3

    def Slutsky_test(self, var=1, alpha=1):
        T = 99999999999
        simpson = self.simpson(lambda t: self.K(var, alpha, t), 0, T, 999999) / T
        K_inf = self.K(var, alpha, T)
        return simpson, K_inf


def h(D, a, sigma, tau):
    #  return (math.pow(4 * D * a, 0.5) / sigma) * math.exp(-a * tau) * (1 - a * tau)
    return np.sqrt(D * np.sqrt(np.pi)) / (a ** 1/4 * sigma) * tau


def K(D, a, tau):
    return D * np.exp(-a * np.abs(tau)) * (1 - a * np.abs(tau))


if __name__ == '__main__':
    process = Processes(h, K)
    process.solve()
