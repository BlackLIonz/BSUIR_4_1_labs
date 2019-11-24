class BRV:
    @staticmethod
    def generate_value(a=214013, m=2 ** 32):
        f = open('A', 'r')
        A = int(f.readline())
        f.close()
        new_A = (a * A) % m
        A = new_A
        f = open('A', 'w')
        f.write(str(A))
        return A / m

    @staticmethod
    def generate(n):
        return [BRV.generate_value() for i in range(n)]

