import math

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2
from scipy.stats import t


def check_equability(k, numbers, start=0, end=1):
    if end == np.inf:
        end = math.ceil(max(numbers))
    interval = (end - start) / k
    dct = {}
    for i in range(int(k)):
        dct[(round(start, 6), round(start + interval, 6))] = \
            len([number for number in numbers if start <= number < start + interval]) / len(numbers)
        start += interval
    return dct


class Random:
    def __init__(self, n):
        self.n = n
        self.mcm_numbers = [self.multiplicative_congruent_method() for i in range(self.n)]
        self.sigma = 1
        self.reversed_numbers = self.reverse_expr(self.expr, self.sigma)

    def reverse_expr(self, expr, sigma):
        number = []
        for num in self.mcm_numbers:
            new_number = expr(num, sigma)
            number.append(new_number)
        return number

    @staticmethod
    def expr(x, sigma=1):
        return math.sqrt(-2 * sigma ** 2 * math.log(1 - x))

    @staticmethod
    def multiplicative_congruent_method(a=214013, m=2 ** 32):
        f = open('A', 'r')
        A = int(f.readline())
        f.close()
        new_A = (a * A) % m
        A = new_A
        f = open('A', 'w')
        f.write(str(A))
        return A / m

    def equability_test(self, k, numbers):
        if numbers is self.mcm_numbers:
            equ = check_equability(k, numbers)
            exp_value = 1 / 2
            dispersion = 1 / 12
        elif numbers is self.reversed_numbers:
            equ = check_equability(k, numbers, 0, np.inf)
            exp_value = math.sqrt(math.pi / 2) * self.sigma
            dispersion = (2 - math.pi / 2) * self.sigma ** 2
        else:
            raise ValueError('Numbers invalid')
        keys = list(equ.keys())
        x = [key[0] for key in keys]
        y = list(equ.values())
        width = keys[0][1] - keys[0][0]
        plt.bar(x, y, width)
        math_value = self.get_exp_value(numbers)
        dispersion_exp = self.get_dispersion(numbers, math_value)
        print(f'{math_value} -> {exp_value}')
        print(f'{dispersion_exp} -> {dispersion}')
        print(f'{self.get_interval_assessment_exp_value(math_value, dispersion, len(numbers))}')
        print(f'{self.get_interval_assessment_dispersion(dispersion, len(numbers))}')
        plt.show()
        
    def pearson_consent_criteria(self, numbers):
        numbers_len = len(numbers)
        if numbers is self.mcm_numbers:
            equ = check_equability(math.sqrt(numbers_len), numbers)
            expr = lambda: 1 / len(equ)
        elif numbers is self.reversed_numbers:
            equ = check_equability(math.sqrt(numbers_len), numbers, 0, np.inf)
            expr = lambda x, sigma=1: (x / (sigma ** 2) * math.exp(-(x * x) / (2 * sigma ** 2)))
        else:
            raise NotImplemented
        sigma = []
        for interval, frequency in equ.items():
            if numbers is self.mcm_numbers:
                p = expr()
            elif numbers is self.reversed_numbers:
                p = expr(interval[1]) - expr(interval[0])
            else:
                raise NotImplemented
            sigma.append(math.pow((frequency - p), 2) / p)
        emp_chi2 = numbers_len * sum(sigma)
        return emp_chi2 < chi2.isf(0.05, len(equ) - 2)


    @staticmethod
    def get_interval_assessment_exp_value(exp_value, dispersion, n, conf_probability=0.95):
        beta = (math.sqrt(dispersion) * t.ppf(conf_probability, n - 1)) / (math.sqrt(n - 1))
        return exp_value - beta, exp_value + beta

    @staticmethod
    def get_interval_assessment_dispersion(dispersion, n, conf_probability=0.95):
        numerator = (n * dispersion)
        return numerator / chi2.isf((1 - conf_probability) / 2, n - 1), \
               numerator / chi2.isf((1 + conf_probability) / 2, n - 1)

    @staticmethod
    def get_exp_value(numbers):
        return sum(numbers) / len(numbers)

    @staticmethod
    def get_dispersion(numbers, m):
        return (1 / (len(numbers) - 1)) * sum([(z - m) ** 2 for z in numbers])

    def independence_test(self, n, s):
        R = 12 / (n - s) * sum([self.mcm_numbers[i] * self.mcm_numbers[i + s] for i in range(n - s)]) - 3
        return R

    def independence_graphic(self, start, stop, step):
        if stop > self.n:
            stop = self.n
        x = range(start, stop, step)
        y = [self.independence_test(x_, 5) for x_ in x]
        plt.plot(x, y)
        plt.show()


if __name__ == '__main__':
    rand = Random(100)
    rand.equability_test(100, rand.reversed_numbers)
    rand.pearson_consent_criteria(rand.mcm_numbers)
    # rand.independence_graphic(100, 10000, 100)
