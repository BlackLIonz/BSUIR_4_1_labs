from hashlib import md5
from os import urandom

from Curve import Curve
from utils import public_key, private_key, hex_decode, bytes_to_long, mod_invert, long_to_bytes

MODE_SIZE = 32

CURVE = (
    hex_decode("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD97"),
    hex_decode("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF6C611070995AD10045841B09B761B893"),
    hex_decode("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFD94"),
    hex_decode("00000000000000000000000000000000000000000000000000000000000000a6"),
    hex_decode("0000000000000000000000000000000000000000000000000000000000000001"),
    hex_decode("8D91E471E0989CDA27DF505A453F2B7635294F2DDF23E3B122ACC99C9E9F1E14"),
)


def sign(curve, private_key, digest):
    q = curve.q
    e = bytes_to_long(digest) % q
    if e == 0:
        e = 1
    while True:
        k = bytes_to_long(urandom(MODE_SIZE)) % q
        if k == 0:
            continue

        r, _ = curve.scalar_multiply(k)
        r %= q
        if r == 0:
            continue

        d = private_key * r
        k *= e
        s = (d + k) % q
        if s == 0:
            continue

        return long_to_bytes(s, MODE_SIZE) + long_to_bytes(r, MODE_SIZE)


def verify(curve, pub, digest, signature):
    q = curve.q
    p = curve.p
    s = bytes_to_long(signature[:MODE_SIZE])
    r = bytes_to_long(signature[MODE_SIZE:])
    if not 0 < r < q or not 0 < s < q:
        return False

    e = bytes_to_long(digest) % curve.q
    if e == 0:
        e = 1
    v = mod_invert(e, q)
    z1 = s * v % q
    z2 = q - r * v % q
    p1x, p1y = curve.scalar_multiply(z1)
    q1x, q1y = curve.scalar_multiply(z2, pub[0], pub[1])

    delta_x = p1x - q1x
    m = (p1y - q1y) * mod_invert(delta_x, p)
    x_c = (m ** 2 - p1x - q1x) % p
    if x_c < 0:
        x_c += p

    R = x_c % q
    return R == r


if __name__ == '__main__':
    message = b"Some kind of a message"

    p, q, a, b, x, y = CURVE
    curve = Curve(p, q, a, b, x, y)

    private_key = private_key(q)
    signature = sign(curve, private_key, md5(message).digest())
    pub = public_key(curve, private_key)
    is_verified = verify(curve, pub, md5(message).digest(), signature)
    print("Is verified", True)
