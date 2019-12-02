from utils import bytes_to_long, mod_invert


class Curve:
    def __init__(self, p, q, a, b, x, y):
        self.p = bytes_to_long(p)
        self.q = bytes_to_long(q)
        self.a = bytes_to_long(a)
        self.b = bytes_to_long(b)
        self.x = bytes_to_long(x)
        self.y = bytes_to_long(y)

        r1 = self.y * self.y % self.p
        r2 = ((self.x * self.x + self.a) * self.x + self.b) % self.p
        if r2 < 0:
            r2 += self.p
        if r1 != r2:
            raise ValueError("Invalid parameters")

    def _pos(self, v):
        if v < 0:
            return v + self.p
        return v

    def _add(self, p1x, p1y, p2x, p2y):
        if p1x == p2x and p1y == p2y:
            t = ((3 * p1x * p1x + self.a) * mod_invert(2 * p1y, self.p)) % self.p
        else:
            tx = self._pos(p2x - p1x) % self.p
            ty = self._pos(p2y - p1y) % self.p
            t = (ty * mod_invert(tx, self.p)) % self.p

        tx = self._pos(t * t - p1x - p2x) % self.p
        ty = self._pos(t * (p1x - tx) - p1y) % self.p
        return tx, ty

    def scalar_multiply(self, degree, x=None, y=None):
        x = x or self.x
        y = y or self.y
        tx = x
        ty = y
        degree -= 1
        if degree == 0:
            raise ValueError("Bad degree value")
        while degree != 0:
            if degree & 1 == 1:
                tx, ty = self._add(tx, ty, x, y)
            degree = degree >> 1
            x, y = self._add(x, y, x, y)
        return tx, ty