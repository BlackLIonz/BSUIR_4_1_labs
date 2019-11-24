from collections import defaultdict

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import scipy.integrate as integrate

from MM.lab2.brv import BRV


def line(text='', length=50):
    if len(text) > 0:
        text = ''.join([' ', text, ' '])
    half = int(length / 2 - len(text))
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
        if by == 'x':
            function = lambda x, y: self.f(x, y) * x
        else:
            function = lambda x, y: self.f(x, y) * y
        return integrate.dblquad(function, self.a, self.b, lambda x: self.a, lambda x: self.b)[0]

    def dispersion(self, array):
        return np.std(array, ddof=1) ** 2

    def theoretical_dispersion(self, mean, by='x'):
        if by == 'x':
            function = lambda x, y: self.f(x, y) * x ** 2
        else:
            function = lambda x, y: self.f(x, y) * y ** 2
        return integrate.dblquad(function, self.a, self.b, lambda x: self.a, lambda x: self.b)[0] - mean ** 2

    def bootstrap(self, stat_func, n, array):
        stats = [stat_func(np.random.choice(array, n, replace=True)) for _ in range(n)]
        var = np.var(stats)
        sigma = np.sqrt(var)
        res = stat_func(array)
        return res - 3 * sigma, res + 3 * sigma

    def solve(self):
        dcrv.histogram()
        x, y = list(zip(*self.pairs))
        mean_x = self.mean(x)
        dispersion_x = self.dispersion(x)
        interval_mean_x = self.bootstrap(np.mean, 100, x)
        interval_dispersion_x = self.bootstrap(np.var, 100, x)

        mean_y = self.mean(y)
        interval_mean_y = self.bootstrap(np.mean, 100, y)
        dispersion_y = self.dispersion(x)
        interval_dispersion_y = self.bootstrap(np.var, 100, y)
        ther_mean_x = self.theoretical_mean('x')
        ther_mean_y = self.theoretical_mean('y')

        print(line('Mean x'))
        print(f'Mean x: {mean_x}')
        print(f'Theoretical mean x: {ther_mean_x}')
        print(f'Interval mean x: {interval_mean_x}')
        print(line('Dispersion x'))
        print(f'Dispersion x: {dispersion_x}')
        print(f'Theoretical dispersion x: {self.theoretical_dispersion(ther_mean_x, "x")}')
        print(f'Interval dispersion x: {interval_dispersion_x}')
        print(line('Mean y'))
        print(f'Mean y: {mean_y}')
        print(f'Theoretical mean y: {ther_mean_y}')
        print(f'Interval mean y: {interval_mean_y}')
        print(line('Dispersion y'))
        print(f'Dispersion y: {dispersion_y}')
        print(f'Theoretical dispersion y: {self.theoretical_dispersion(ther_mean_y, "y")}')
        print(f'Interval dispersion y: {interval_dispersion_y}')
        print(line('Correlations'))
        print(f'Correlation matrix:\n{np.corrcoef(x, y)}')
        print(line())


if __name__ == '__main__':
    f = lambda x, y: (12 / 7) * (x ** 2 + y / 2)
    a = 0
    b = 1
    max_value = 18 / 7
    dcrv = DCRV(f, a, b, max_value, 10000)
    dcrv.solve()
