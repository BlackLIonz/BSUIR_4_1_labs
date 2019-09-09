import unittest
import numpy as np
from main import DualSimplexMethod


class TestDualSimplexMethod(unittest.TestCase):
    #
    # def test_case_one(self):
    #     A = np.array([[1, -5, 3, 1, 0, 0],
    #                   [4, -1, 1, 0, 1, 0],
    #                   [2, 4, 2, 0, 0, 1]])
    #     c = np.array([7, -2, 6, 0, 5, 2])
    #     b = np.array([-7, 22, 30])
    #     d_down_asterisk = [2, 1, 0, 0, 1, 1]
    #     d_up_asterisk = [6, 6, 5, 2, 4, 6]
    #     ds = DualSimplexMethod(A, c, b, d_down_asterisk, d_up_asterisk)
    #     self.assertEqual(ds.solve(), ([5, 3, 1, 0, 4, 6], 67))

    def test_case_two(self):
        A = np.array([[1, 0, 2, 2, -3, 3],
                      [0, 1, 0, -1, 0, 1],
                      [1, 0, 1, 3, 2, 1]])
        c = np.array([3, 0.5, 4, 4, 1, 5])
        b = np.array([15, 0, 13])
        d_down_asterisk = [0, 0, 0, 0, 0, 0]
        d_up_asterisk = [3, 5, 4, 3, 3, 5]
        ds = DualSimplexMethod(A, c, b, d_down_asterisk, d_up_asterisk)
        self.assertEqual(ds.solve(), ([3, 0, 4, 1.1818, 0.6364, 1.1818], 36.2727))

    def test_case_three(self):
        A = np.array([[1, 0, 0, 12, 1, -3, 4, -1],
                      [0, 1, 0, 11, 12, 3, 5, 3],
                      [0, 0, 1, 1, 0, 22, -2, 1]])
        c = np.array([2, 1, -2, -1, 4, -5, 5, 5])
        b = np.array([40, 107, 61])
        d_down_asterisk = [0, 0, 0, 0, 0, 0]
        d_up_asterisk = [3, 5, 5, 3, 4, 6, 3]
        ds = DualSimplexMethod(A, c, b, d_down_asterisk, d_up_asterisk)
        self.assertEqual(ds.solve(), ([3, 5, 0, 1.8779, 2.7545, 3.0965, 6, 3], 49.6577))


if __name__ == '__main__':
    unittest.main()
