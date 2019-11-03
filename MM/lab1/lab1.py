import math
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import chi2, t, chisquare


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
        self.bsv_numbers = [self.multiplicative_congruent_method() for i in range(self.n)]
        self.sigma = 1
        self.urv_numbers = self.reverse_expr(self.expr, self.sigma)
        self.distribution_table = dict(((0, 0.25), (1, 0.5), (2, 0.25)))
        self.discrete_numbers = self.discrete_generator(self.distribution_table)

    def reverse_expr(self, expr, sigma):
        number = []
        for num in self.bsv_numbers:
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

    def discrete_generator(self, distribution_table):
        res = []
        probabilities = [sum(list(distribution_table.values())[:i + 1]) for i in range(len(distribution_table))]
        intervals = dict(zip(distribution_table.keys(), probabilities))
        for rand_number in self.bsv_numbers:
            for num, probability in intervals.items():
                if rand_number <= probability:
                    res.append(num)
                    break
        return res

    def equability_test(self, k, numbers):
        if numbers is self.bsv_numbers:
            equ = check_equability(k, numbers)
            exp_value = 1 / 2
            dispersion_exp = 1 / 12
        elif numbers is self.urv_numbers:
            equ = check_equability(k, numbers, 0, np.inf)
            exp_value = math.sqrt(math.pi / 2) * self.sigma
            dispersion_exp = (2 - math.pi / 2) * self.sigma ** 2
        elif numbers is self.discrete_numbers:
            equ = check_equability(len(self.distribution_table), numbers, 0, 3)
            exp_value = sum([x * p for x, p in self.distribution_table.items()])
            dispersion_exp = sum([x ** 2 * p for x, p in self.distribution_table.items()]) - exp_value ** 2
        else:
            raise NotImplemented
        keys = list(equ.keys())
        x = [key[0] for key in keys]
        y = list(equ.values())
        width = keys[0][1] - keys[0][0]
        plt.bar(x, y, width)
        math_value = self.get_exp_value(numbers)
        dispersion = self.get_dispersion(numbers, math_value)
        print(f'M: {math_value} -> {exp_value}')
        print(f'M: {self.get_interval_assessment_exp_value(math_value, dispersion, len(numbers))}')
        print(f'D: {dispersion} -> {dispersion_exp}')
        print(f'D: {self.get_interval_assessment_dispersion(dispersion, len(numbers))}')
        plt.show()

    def pearson_consent_criteria(self, numbers):
        numbers_len = len(numbers)
        if numbers is self.bsv_numbers:
            equ = check_equability(math.sqrt(numbers_len), numbers)
            expression = lambda x: x
        elif numbers is self.urv_numbers:
            equ = check_equability(math.sqrt(numbers_len), numbers, 0, np.inf)
            expression = lambda x, sigma=1: 1 - math.exp(-(x ** 2) / (2 * sigma ** 2))
        elif numbers is self.discrete_numbers:
            equ = check_equability(len(self.distribution_table),
                                   numbers,
                                   min(self.distribution_table.keys()),
                                   max(self.distribution_table.keys()) + 1)
            expression = lambda x: self.distribution_table[x]
        else:
            raise NotImplemented
        sigma = []
        equ_first = next(iter(equ))
        p = expression(equ_first[1]) - expression(equ_first[0])
        for interval, frequency in equ.items():
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
        R = 12 / (n - s) * sum([self.bsv_numbers[i] * self.bsv_numbers[i + s] for i in range(n - s)]) - 3
        return R

    def independence_graphic(self, start, stop, step=10):
        if stop > self.n:
            stop = self.n
        x = range(start, stop, step)
        y = [self.independence_test(x_, 5) for x_ in x]
        plt.plot(x, y)
        plt.show()

    def discrete_chi2_test(self, dist, expected, y=0.95):
        counter_dist = list(Counter(dist).items())
        sorted_counter_dist = sorted(counter_dist, key=lambda x: x[0])
        count_list = [item[1] for item in sorted_counter_dist]
        _, p_val = chisquare(count_list, f_exp=expected)
        return p_val, p_val >= 1 - y


def line():
    print('=' * 50)


if __name__ == '__main__':
    line()
    rand = Random(1000)
    rand.equability_test(100, rand.bsv_numbers)
    rand.independence_graphic(100, 1000, 100)
    print('Pearson: ', rand.pearson_consent_criteria(rand.bsv_numbers))
    line()
    rand.equability_test(100, rand.urv_numbers)
    print('Pearson: ', rand.pearson_consent_criteria(rand.urv_numbers))
    line()
    rand.equability_test(100, rand.discrete_numbers)
    print('Pearson: ', rand.discrete_chi2_test(rand.discrete_numbers, [250, 500, 250]))
