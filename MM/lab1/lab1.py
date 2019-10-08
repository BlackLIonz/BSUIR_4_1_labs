import matplotlib.pyplot as plt
import math
import numpy as np


class Random:
    def __init__(self, n):
        self.n = n
        self.mcm_numbers = [self.multiplicative_congruent_method() for i in range(self.n)]
        self.reversed_numbers = self.reverse_expr()

    def reverse_expr(self, sigma=1):
        number = []
        for num in self.mcm_numbers:
            new_number = -math.pow(2, 0.5) * sigma * math.pow(math.log(-1/(num - 1)), 0.5)
            number.append(new_number)
        return number

    @staticmethod
    def multiplicative_congruent_method(a=214013, m=2**32):
        f = open('A', 'r')
        A = int(f.readline())
        f.close()
        new_A = (a * A) % m
        A = new_A
        f = open('A', 'w')
        f.write(str(A))
        return A / m

    def continuous_random_variable(self, n):
        pass

    def check_equability(self, k, n):
        interval = 1 / k
        start = 0
        dct = {}
        for i in range(k):
            dct[(round(start, 6), round(start + interval, 6))] = len([number for number in self.mcm_numbers if start <= number < start + interval]) / n
            start += interval
        return dct

    def equability_test(self, k, n):
        equ= self.check_equability(k, n)
        keys = list(equ.keys())
        x = [key[0] for key in keys]
        y = list(equ.values())
        width = keys[0][1] - keys[0][0]
        plt.bar(x, y, width)
        m = sum(self.mcm_numbers) / n
        S = ((1 / (n - 1)) * sum([(z - m) ** 2 for z in self.mcm_numbers]))
        print(f'{m} -> 1/2 = 0.5')
        print(f'{S} -> 1/12 = 0.083333')
        plt.show()

    def random_test(self):
        pass

    def independence_test(self, n, s):
        R = 12 / (n - s) * sum([self.mcm_numbers[i] * self.mcm_numbers[i + s] for i in range(n - s)]) - 3
        print(f'{R} -> 0, n -> inf')
        return R

    def independence_graphic(self, start, stop, step):
        if stop > self.n:
            stop = self.n
        x = range(start, stop, step)
        y = [self.independence_test(x_, 5) for x_ in x]
        plt.plot(x, y)
        plt.show()


if __name__ == '__main__':
    rand = Random(1000)
    rand.independence_graphic(10, 1000, 10)
