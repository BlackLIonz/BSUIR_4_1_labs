import matplotlib.pyplot as plt
import numpy as np


def multiplicative_congruent_method(a=214013, m=2**32):
    f = open('A', 'r')
    A = int(f.readline())
    f.close()
    new_A = (a * A) % m
    A = new_A
    f = open('A', 'w')
    f.write(str(A))
    return A / m


def check_equability(k, n):
    interval = 1 / k
    numbers = [multiplicative_congruent_method() for i in range(n)]
    start = 0
    dct = {}
    for i in range(k):
        dct[(round(start, 6), round(start + interval, 6))] = len([number for number in numbers if start <= number < start + interval]) / n
        start += interval
    return dct, numbers


def print_histogram_equability(k, n):
    equ, numbers = check_equability(k, n)
    keys = list(equ.keys())
    x = [key[0] for key in keys]
    y = list(equ.values())
    width = keys[0][1] - keys[0][0]
    plt.bar(x, y, width)
    m = sum(numbers) / n
    S = ((1 / (n - 1)) * sum([(z - m) ** 2 for z in numbers]))
    print(f'{m} -> 1/2 = 0.5')
    print(f'{S} -> 1/12 = 0.083333')
    plt.show()


if __name__ == '__main__':
    print_histogram_equability(10, 1000)
