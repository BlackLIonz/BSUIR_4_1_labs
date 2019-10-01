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
        dct[(round(start, 6), round(start + interval, 6))] = len([number for number in numbers if start < number < start + interval]) / n
        start += interval
    return dct


if __name__ == '__main__':
    res = check_equability(10, 100)
    print(res)
