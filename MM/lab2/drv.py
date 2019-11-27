
from MM.lab2.brv import BRV
from MM.lab2.dcrv import DCRV


class DRV(DCRV):
    def __init__(self, function, interval_start, interval_end, function_maximum, n):
        super().__init__(function, interval_start, interval_end, function_maximum, n)

    def generate_pair(self):
        x, y = BRV.generate(2)
        return self.f(x), self.f(y)

    def theoretical_mean(self, by='x'):
        # return 1/2 * 0 + 1/2 * 1
        return 1/3 * 0 + 1/3 * 1 + 1/3 * 2

    def theoretical_dispersion(self, mean, by='x'):
        mean = self.theoretical_mean()
        # return 1/2 * (0 - mean) ** 2 + 1/2 * (1 - mean) ** 2
        return 1/3 * (0 - mean) ** 2 + 1/3 * (1 - mean) ** 2 + 1/3 * (2 - mean) ** 2


def f(x):
    if x <= 1 / 3:
        return 0
    elif x <= 2 / 3:
        return 1
    else:
        return 2

# def f(x):
#     if x <= 1/2:
#         return 0
#     else:
#         return 1


if __name__ == '__main__':
    a = 0
    b = 1
    max_value = 2
    drv = DRV(f, a, b, max_value, 100)
    drv.generate_pairs()
    drv.full_stats()
