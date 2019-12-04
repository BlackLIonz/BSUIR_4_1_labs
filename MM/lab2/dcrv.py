from collections import defaultdict

import matplotlib.pyplot as plt
import numpy as np
import scipy.integrate as integrate
import scipy.stats as sp
from mpl_toolkits.mplot3d import Axes3D

from MM.lab2.brv import BRV


def line(text='', length=50):
    if len(text) > 0:
        text = ''.join([' ', text, ' '])
    half = int((length - int(len(text))) / 2)
    return ''.join(['=' * half, text, '=' * (length - half - len(text))])


class DCRV:
    def __init__(self, function, interval_start, interval_end, function_maximum, n):
        self.f = function
        self.a = interval_start
        self.b = interval_end
        self.max_value = function_maximum
        self.n = n
        self.pairs = None

    def generate_pair(self):
        pair = np.array(BRV.generate(2))
        max_values = BRV.generate_value() * self.max_value
        return pair if self.f(*pair) >= max_values else self.generate_pair()

    def generate_pairs(self):
        self.pairs = [tuple(self.generate_pair()) for _ in range(self.n)]

    def counter(self, interval_count):
        counter = defaultdict(lambda: 0)
        step = (self.b - self.a) / interval_count
        for i in range(interval_count):
            for j in range(interval_count):
                for x, y in self.pairs:
                    if i * step < x < (i + 1) * step and j * step < y < (j + 1) * step:
                        counter[(round((2 * i + 1) * step, 6), round((2 * j + 1) * step), 6)] += 1
        return dict(counter)

    def histogram(self):
        x, y = list(zip(*self.pairs))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        hist, x_edges, y_edges = np.histogram2d(x, y, range=[[0, 1], [0, 1]], density=True)

        x_pos, y_pos = np.meshgrid(x_edges[:-1], y_edges[:-1], indexing="ij")
        x_pos = x_pos.ravel()
        y_pos = y_pos.ravel()
        z_pos = 0

        dx = dy = 0.1 * np.ones_like(z_pos)
        dz = hist.ravel() / self.n

        ax.bar3d(x_pos, y_pos, z_pos, dx, dy, dz, zsort='average')
        plt.show()

    @staticmethod
    def mean(array):
        return np.mean(array)

    def theoretical_mean(self, by='x'):
        return integrate.dblquad(lambda x, y: self.f(x, y) * (eval(by)),
                                 self.a, self.b, lambda x: self.a, lambda x: self.b)[0]

    @staticmethod
    def dispersion(array):
        return np.std(array, ddof=1) ** 2

    def theoretical_dispersion(self, mean, by='x'):
        return integrate.dblquad(lambda x, y: self.f(x, y) * (eval(by)) ** 2,
                                 self.a, self.b, lambda x: self.a, lambda x: self.b)[0] - mean ** 2

    @staticmethod
    def bootstrap(stat_func, n, array):
        stats = [stat_func(np.random.choice(array, n, replace=True)) for _ in range(n)]
        var = np.var(stats)
        sigma = np.sqrt(var)
        res = stat_func(array)
        return res - 3 * sigma, res + 3 * sigma

    def correlation(self):
        x, y = list(zip(*self.pairs))
        mean_xy = np.mean([x * y for x, y in self.pairs])
        mean_x = self.mean(x)
        dispersion_x = self.dispersion(x)
        mean_y = self.mean(y)
        dispersion_y = self.dispersion(x)
        return self.cov(mean_xy, mean_x, mean_y) / (np.sqrt(dispersion_x * dispersion_y))

    def theoretical_correlation(self):
        t_mean_x = self.theoretical_mean('x')
        t_mean_y = self.theoretical_mean('y')
        t_mean_xy = self.theoretical_mean('x * y')
        t_var_x = self.theoretical_dispersion(t_mean_x, 'x')
        t_var_y = self.theoretical_dispersion(t_mean_y, 'y')
        return self.cov(t_mean_xy, t_mean_x, t_mean_y) / (np.sqrt(t_var_x * t_var_y))

    @staticmethod
    def cov(xy, x, y):
        return xy - x * y

    def z_test(self, mean, t_mean, t_var):
        z = (mean - t_mean) / (np.sqrt(t_var / len(self.pairs)))
        p_val = sp.norm.sf(np.fabs(z)) * 2
        return p_val > 0.05, p_val

    @staticmethod
    def fisher_transformation(estimate):
        return 1 / 2 * np.log((1 + estimate) / (1 - estimate))

    def wald_test(self, array, theoretical_estimate, function):
        var = self.dispersion(array)
        stats = [function(np.random.choice(array, 100, replace=True)) for _ in range(100)]
        var_estimate = np.var(stats)
        wald = (var - theoretical_estimate) ** 2 / var_estimate
        p_val = sp.chi2.sf(wald, 1)
        return p_val > 0.05, p_val

    def full_stats(self):
        self.generate_pairs()
        self.histogram()

        x, y = list(zip(*self.pairs))
        mean_x = self.mean(x)
        dispersion_x = self.dispersion(x)
        interval_mean_x = self.bootstrap(self.mean, 100, x)
        interval_dispersion_x = self.bootstrap(self.dispersion, 100, x)

        mean_y = self.mean(y)
        dispersion_y = self.dispersion(y)
        interval_mean_y = self.bootstrap(self.mean, 100, y)
        interval_dispersion_y = self.bootstrap(self.dispersion, 100, y)

        correlation = self.correlation()

        theoretical_mean_x = self.theoretical_mean('x')
        theoretical_mean_y = self.theoretical_mean('y')
        theoretical_var_x = self.theoretical_dispersion(theoretical_mean_x, "x")
        theoretical_var_y = self.theoretical_dispersion(theoretical_mean_y, "y")
        theoretical_correlation = self.theoretical_correlation()

        print(line('Mean x'))
        print(f'Mean x: {mean_x}')
        print(f'Theoretical mean x: {theoretical_mean_x}')
        print(f'Interval mean x: {interval_mean_x}')
        print(line('Dispersion x'))
        print(f'Dispersion x: {dispersion_x}')
        print(f'Theoretical dispersion x: {theoretical_var_x}')
        print(f'Interval dispersion x: {interval_dispersion_x}')
        print(line('Mean y'))
        print(f'Mean y: {mean_y}')
        print(f'Theoretical mean y: {theoretical_mean_y}')
        print(f'Interval mean y: {interval_mean_y}')
        print(line('Dispersion y'))
        print(f'Dispersion y: {dispersion_y}')
        print(f'Theoretical dispersion y: {theoretical_var_y}')
        print(f'Interval dispersion y: {interval_dispersion_y}')
        print(line('Correlations'))
        print(f'Correlation: {correlation}')
        print(f'Theoretical correlation: {theoretical_correlation}')
        print(f'Correlation matrix:\n{np.corrcoef(x, y)}')
        print(line('Z-test for mean'))
        print(f'Z-test x: {self.z_test(mean_x, theoretical_mean_x, theoretical_var_x)}')
        print(f'Z-test y: {self.z_test(mean_y, theoretical_mean_y, theoretical_var_y)}')
        print(line('Wald test for var'))
        print(f'Wald test for var x: {self.wald_test(x, theoretical_var_x, np.var)}')
        print(f'Wald test for var y: {self.wald_test(y, theoretical_var_y, np.var)}')
        print(line('Z-test for correlation'))
        print(f'Z-test: {self.z_test(correlation, theoretical_correlation, theoretical_var_x)}')
        print(line())


def f(x, y):
    return (12 / 7) * (x ** 2 + y / 2)


if __name__ == '__main__':
    a = 0
    b = 1
    max_value = 18 / 7
    random_vector = DCRV(f, a, b, max_value, 10000)
    random_vector.full_stats()
