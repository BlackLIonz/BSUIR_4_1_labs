from codecs import getdecoder
from codecs import getencoder
from os import urandom

_hexdecoder = getdecoder("hex")
_hexencoder = getencoder("hex")


def hex_decode(data):
    return _hexdecoder(data)[0]


def hex_encode(data):
    return _hexencoder(data)[0].decode("ascii")


def str_xor(a, b):
    return bytes(a_i ^ b_i for a_i, b_i in zip(bytearray(a), bytearray(b)))


def bytes_to_long(raw):
    return int(hex_encode(raw), 16)


def long_to_bytes(n, size=32):
    res = hex(int(n))[2:].rstrip("L")
    if len(res) % 2 != 0:
        res = "0" + res
    s = hex_decode(res)
    if len(s) != size:
        s = (size - len(s)) * b"\x00" + s
    return s


def mod_invert(a, n):
    """
    # k^-1 = p - (-k)^-1 mod p
    """

    if a < 0:
        return n - mod_invert(-a, n)
    t, new_t = 0, 1
    r, new_r = n, a
    while new_r:
        quotinent = r // new_r
        t, new_t = new_t, t - quotinent * new_t
        r, new_r = new_r, r - quotinent * new_r
    if r > 1:
        return -1
    if t < 0:
        t += n
    return t


def public_key(curve, private_key):
    return curve.scalar_multiply(private_key)


def private_key(q):
    key = bytes_to_long(urandom(32))
    while not key or key >= bytes_to_long(q):
        key = bytes_to_long(urandom(32))
    return key
