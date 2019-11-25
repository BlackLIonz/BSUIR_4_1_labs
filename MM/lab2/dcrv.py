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
    def __init__(self, f, a, b, max_value, n):
        self.f = f
        self.a = a
        self.b = b
        self.max_value = max_value
        self.n = n
        self.pairs = self.generate_pairs(n)

    def generate_pair(self):
        pair = np.array(BRV.generate(2))
        max_value = BRV.generate_value() * self.max_value
        return pair if self.f(*pair) >= max_value else self.generate_pair()

    def generate_pairs(self, n):
        return [tuple(self.generate_pair()) for i in range(n)]

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
        data = list(zip(*self.pairs))
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        x = data[0]
        y = data[1]
        hist, xedges, yedges = np.histogram2d(x, y, bins=32, range=[[0, 1], [0, 1]], density=True)

        xpos, ypos = np.meshgrid(xedges[:-1], yedges[:-1], indexing="ij")
        xpos = xpos.ravel()
        ypos = ypos.ravel()
        zpos = 0

        dx = dy = 0.1 * np.ones_like(zpos)
        dz = hist.ravel()

        ax.bar3d(xpos, ypos, zpos, dx, dy, dz, zsort='average')
        plt.show()

    def mean(self, array):
        return np.mean(array)

    def theoretical_mean(self, by='x'):
        function = lambda x, y: self.f(x, y) * (eval(by))
        return integrate.dblquad(function, self.a, self.b, lambda x: self.a, lambda x: self.b)[0]

    def dispersion(self, array):
        return np.std(array, ddof=1) ** 2

    def theoretical_dispersion(self, mean, by='x'):
        function = lambda x, y: self.f(x, y) * (eval(by)) ** 2
        return integrate.dblquad(function, self.a, self.b, lambda x: self.a, lambda x: self.b)[0] - mean ** 2

    def bootstrap(self, stat_func, n, array):
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

    def cov(self, xy, x, y):
        return xy - x * y

    def z_test(self, mean, t_mean, t_var):
        z = (mean - t_mean) / (np.sqrt(t_var / len(self.pairs)))
        pval = sp.norm.sf(np.fabs(z)) * 2
        return pval > 0.05, pval

    def fisher_transformation(self, estimate):
        return 1/2 * np.log((1 + estimate) / (1 - estimate))

    def wald_test(self, array, theoretical_estimate, function):
        var = self.dispersion(array)
        stats = [function(np.random.choice(array, 100, replace=True)) for _ in range(100)]
        var_estimate = np.var(stats)
        wald = (var - theoretical_estimate) ** 2 / var_estimate
        pval = sp.chi2.sf(wald, 1)
        return pval > 0.05, pval

    def solve(self):
        dcrv.histogram()
        x, y = list(zip(*self.pairs))
        mean_x = self.mean(x)
        dispersion_x = self.dispersion(x)
        interval_mean_x = self.bootstrap(np.mean, 100, x)
        interval_dispersion_x = self.bootstrap(np.var, 100, x)

        mean_y = self.mean(y)
        dispersion_y = self.dispersion(y)
        interval_mean_y = self.bootstrap(np.mean, 100, y)
        interval_dispersion_y = self.bootstrap(np.var, 100, y)
        ther_mean_x = self.theoretical_mean('x')
        ther_mean_y = self.theoretical_mean('y')
        ther_var_x = self.theoretical_dispersion(ther_mean_x, "x")
        ther_var_y = self.theoretical_dispersion(ther_mean_y, "y")
        theoretical_correlation = self.theoretical_correlation()
        correlation = self.correlation()

        print(line('Mean x'))
        print(f'Mean x: {mean_x}')
        print(f'Theoretical mean x: {ther_mean_x}')
        print(f'Interval mean x: {interval_mean_x}')
        print(line('Dispersion x'))
        print(f'Dispersion x: {dispersion_x}')
        print(f'Theoretical dispersion x: {ther_var_x}')
        print(f'Interval dispersion x: {interval_dispersion_x}')
        print(line('Mean y'))
        print(f'Mean y: {mean_y}')
        print(f'Theoretical mean y: {ther_mean_y}')
        print(f'Interval mean y: {interval_mean_y}')
        print(line('Dispersion y'))
        print(f'Dispersion y: {dispersion_y}')
        print(f'Theoretical dispersion y: {ther_var_y}')
        print(f'Interval dispersion y: {interval_dispersion_y}')
        print(line('Correlations'))
        print(f'Correlation: {correlation}')
        print(f'Theoretical correlation: {theoretical_correlation}')
        print(f'Correlation matrix:\n{np.corrcoef(x, y)}')
        print(line('Z-test for mean'))
        print(f'Z-test x: {self.z_test(mean_x, ther_mean_x, ther_var_x)}')
        print(f'Z-test y: {self.z_test(mean_y, ther_mean_y, ther_var_y)}')
        print(line('Wald test for var'))
        print(f'Wald test for var x: {self.wald_test(x, ther_var_x, np.var)}')
        print(f'Wald test for var y: {self.wald_test(y, ther_var_y, np.var)}')
        print(line('Z-test for correlation'))
        print(f'Z-test: {self.z_test(correlation, theoretical_correlation, ther_var_x)}')
        print(line())


if __name__ == '__main__':
    f = lambda x, y: (12 / 7) * (x ** 2 + y / 2)
    a = 0
    b = 1
    max_value = 18 / 7
    dcrv = DCRV(f, a, b, max_value, 10000)
    dcrv.solve()
