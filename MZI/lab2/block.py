import numpy as np


class Block:
    def __init__(self, text, key):
        self.H = np.array([
            [0xB1, 0x94, 0xBA, 0xC8, 0x0A, 0x08, 0xF5, 0x3B, 0x36, 0x6D, 0x00, 0x8E, 0x58, 0x4A, 0x5D, 0xE4],
            [0x85, 0x04, 0xFA, 0x9D, 0x1B, 0xB6, 0xC7, 0xAC, 0x25, 0x2E, 0x72, 0xC2, 0x02, 0xFD, 0xCE, 0x0D],
            [0x5B, 0xE3, 0xD6, 0x12, 0x17, 0xB9, 0x61, 0x81, 0xFE, 0x67, 0x86, 0xAD, 0x71, 0x6B, 0x89, 0x0B],
            [0x5C, 0xB0, 0xC0, 0xFF, 0x33, 0xC3, 0x56, 0xB8, 0x35, 0xC4, 0x05, 0xAE, 0xD8, 0xE0, 0x7F, 0x99],  #
            [0xE1, 0x2B, 0xDc, 0x1A, 0xE2, 0x82, 0x57, 0xEC, 0x70, 0x3F, 0xCC, 0xF0, 0x95, 0xEE, 0x8D, 0xF1],
            [0xC1, 0xAB, 0x76, 0x38, 0x9F, 0xE6, 0x78, 0xCA, 0xF7, 0xC6, 0xF8, 0x60, 0xD5, 0xBB, 0x9C, 0x4F],
            [0xF3, 0x3C, 0x65, 0x7B, 0x63, 0x7C, 0x30, 0x6A, 0xDD, 0x4E, 0xA7, 0x79, 0x9E, 0xB2, 0x3D, 0x31],
            [0x3E, 0x98, 0xB5, 0x6E, 0x27, 0xD3, 0xBC, 0xCF, 0x59, 0x1E, 0x18, 0x1F, 0x4C, 0x5A, 0xB7, 0x93],
            [0xE9, 0xDE, 0xE7, 0x2C, 0x8F, 0x0C, 0x0F, 0xA6, 0x2D, 0xD8, 0x49, 0xF4, 0x6F, 0x73, 0x96, 0x47],
            [0x06, 0x07, 0x53, 0x16, 0xED, 0x24, 0x7A, 0x37, 0x39, 0xCB, 0xA3, 0x83, 0x03, 0xA9, 0x8B, 0xF6],
            [0x92, 0xBD, 0x9B, 0x1C, 0xE5, 0xD1, 0x41, 0x01, 0x54, 0x45, 0xFB, 0xC9, 0x5E, 0x4D, 0x0E, 0xF2],
            [0x68, 0x20, 0x80, 0xAA, 0x22, 0x7D, 0x64, 0x2F, 0x26, 0x87, 0xF9, 0x34, 0x90, 0x40, 0x55, 0x11],
            [0xBE, 0x32, 0x97, 0x13, 0x43, 0xFC, 0x9A, 0x48, 0xA0, 0x2A, 0x88, 0x5F, 0x19, 0x4B, 0x09, 0xA1],
            [0x7E, 0xCD, 0xA4, 0xD0, 0x15, 0x44, 0xAF, 0x8C, 0xA5, 0x84, 0x50, 0xBF, 0x66, 0xD2, 0xE8, 0x8A],
            [0xA2, 0xD7, 0x46, 0x52, 0x42, 0xA8, 0xDf, 0xB3, 0x69, 0x74, 0xC5, 0x51, 0xEB, 0x23, 0x29, 0x21],
            [0xD4, 0xEF, 0xD9, 0xB4, 0x3A, 0x62, 0x28, 0x75, 0x91, 0x14, 0x10, 0xEA, 0x77, 0x6C, 0xDA, 0x1D]
        ])
        self.text = self._prepare_text(text)
        self.key = self._prepare_key(key)

    def encrypt(self):
        a, b, c, d = self.text
        for i in range(1, 9):
            b = self.xor(b, self.transformation_G(5, self.plus(a, self.key[(7*i - 6) % 8])))
            c = self.xor(c, self.transformation_G(21, self.plus(d, self.key[(7*i - 5) % 8])))
            a = self.minus(a, self.transformation_G(13, self.plus(d, self.key[(7*i - 4) % 8])))
            e = self.xor(self.transformation_G(21, self.plus(self.plus(b, c), self.key[(7*i - 3) % 8])),
                         self.int_to_binary(i % 2 ** 32))
            b = self.plus(b, e)
            c = self.minus(c, e)
            d = self.plus(d, self.transformation_G(13, self.plus(c, self.key[(7*i - 2) % 8])))
            b = self.xor(b, self.transformation_G(21, self.plus(a, self.key[(7*i - 1) % 8])))
            c = self.xor(c, self.transformation_G(5, self.plus(d, self.key[(7*i) % 8])))
            a, b, c, d = c, a, d, b
        Y = ''.join([b, d, a, c])
        return Y

    def decrypt(self, text):
        a, b, c, d = self.chunk_it(text, 4)
        for i in range(8, 0, -1):
            b = self.xor(b, self.transformation_G(5, self.plus(a, self.key[(7 * i) % 8])))
            c = self.xor(c, self.transformation_G(21, self.plus(d, self.key[(7 * i - 1) % 8])))
            a = self.minus(a, self.transformation_G(13, self.plus(d, self.key[(7 * i - 2) % 8])))
            e = self.xor(self.transformation_G(21, self.plus(self.plus(b, c), self.key[(7 * i - 3) % 8])),
                         self.int_to_binary(i % 2 ** 32))
            b = self.plus(b, e)
            c = self.minus(c, e)
            d = self.plus(d, self.transformation_G(13, self.plus(c, self.key[(7 * i - 4) % 8])))
            b = self.xor(b, self.transformation_G(21, self.plus(a, self.key[(7 * i - 5) % 8])))
            c = self.xor(c, self.transformation_G(5, self.plus(d, self.key[(7 * i - 6) % 8])))
            a, b, c, d = b, d, a, c
        Y = ''.join([c, a, d, b])
        letters = self.chunk_it(Y, len(Y) / 8)

        return Y

    def plus(self, a, b):
        res = (int(a, 2) + int(b, 2)) % 2 ** 32
        res_binary = self.int_to_binary(res)
        return res_binary

    def minus(self, a, b):
        res = (int(a, 2) - int(b, 2)) % 2 ** 32
        res_binary = self.int_to_binary(res)
        if len(res_binary) > 32:
            raise ValueError('Binary minus bigger that 128')
        return res_binary

    def xor(self, a, b):
        xor = int(a, 2) ^ int(b, 2)
        binary_xor = self.int_to_binary(xor)
        return binary_xor

    def transformation_G(self, r, u):
        us = self.chunk_it(u, 4)
        res = []
        for u in us:
            h = self.get_H(u)
            res.append(self.int_to_binary(h))
        res = ''.join(res)
        res = self.shift(res, r)
        return res

    @staticmethod
    def shift(string, steps):
        lst = string[steps:] + string[:steps]
        return lst

    @staticmethod
    def int_to_binary(num):
        binary_num = '{0:b}'.format(num)
        for length in [8, 16, 32]:
            if len(binary_num) < length:
                binary_num = '0' * (length - (len(binary_num))) + str(binary_num)
                break
            elif len(binary_num) == length:
                break
        return binary_num

    @staticmethod
    def string_to_binary(string):
        return ''.join([f"0{format(ord(i), 'b')}" for i in string])

    def get_H(self, u):
        hexed_u = hex(int(u, 2))
        a, b = hexed_u[-2:]
        if a == 'x':
            a = '0'
        H_value = self.H[int(a, 16), int(b, 16)]
        return H_value

    @staticmethod
    def chunk_it(seq, num):
        avg = len(seq) / float(num)
        out = []
        last = 0.0
        while last < len(seq):
            out.append(seq[int(last):int(last + avg)])
            last += avg
        return out

    def _prepare_key(self, key):
        if len(key) * 8 > 256:
            raise ValueError('Key to long')
        return self.chunk_it(self.string_to_binary(key), 8)

    def _prepare_text(self, text):
        if len(text) * 8 > 128:
            raise ValueError('Text to long')
        return self.chunk_it(self.string_to_binary(text), 4)


block = Block('HelloWorldHelloW', 'SomeKeySomeKeySomeKeySomeKeySome')
a = block.encrypt()
print(''.join(block.text))
print(block.decrypt(a))
