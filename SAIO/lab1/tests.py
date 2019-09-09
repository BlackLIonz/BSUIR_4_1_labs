import unittest
import numpy as np
import sys
import os
from SAIO.lab1.dual_simplex_method import DualSimplexMethod

sys.stdout = open("logger.txt", "w+")


class TestDualSimplexMethod(unittest.TestCase):

    def test_case_zero(self):
        A = np.array([[2, 1, -1, 0, 0, 1],
                      [1, 0, 1, 1, 0, 0],
                      [0, 1, 0, 0, 1, 0]])
        c = np.array([3, 2, 0, 3, -2, -4])
        b = np.array([2, 5, 0])
        d_down_asterisk = [0, -1, 2, 1, -1, 0]
        d_up_asterisk = [2, 4, 4, 3, 3, 5]
        ds = DualSimplexMethod(A, c, b, d_down_asterisk, d_up_asterisk)
        self.assertEqual(([1.5, 1, 2, 1.5, -1, 0], 13), ds.solve())

    def test_case_one(self):
        A = np.array([[1, -5, 3, 1, 0, 0],
                      [4, -1, 1, 0, 1, 0],
                      [2, 4, 2, 0, 0, 1]])
        c = np.array([7, -2, 6, 0, 5, 2])
        b = np.array([-7, 22, 30])
        d_down_asterisk = [2, 1, 0, 0, 1, 1]
        d_up_asterisk = [6, 6, 5, 2, 4, 6]
        ds = DualSimplexMethod(A, c, b, d_down_asterisk, d_up_asterisk)
        self.assertEqual(([5, 3, 1, 0, 4, 6], 67), ds.solve())

    def test_case_two(self):
        A = np.array([[1, 0, 2, 2, -3, 3],
                      [0, 1, 0, -1, 0, 1],
                      [1, 0, 1, 3, 2, 1]])
        c = np.array([3, 0.5, 4, 4, 1, 5])
        b = np.array([15, 0, 13])
        d_down_asterisk = [0, 0, 0, 0, 0, 0]
        d_up_asterisk = [3, 5, 4, 3, 3, 5]
        ds = DualSimplexMethod(A, c, b, d_down_asterisk, d_up_asterisk)
        self.assertEqual(([3, 0, 4, 1.1818, 0.6364, 1.1818], 36.2726), ds.solve())

    def test_case_three(self):
        A = np.array([[1, 0, 0, 12, 1, -3, 4, -1],
                      [0, 1, 0, 11, 12, 3, 5, 3],
                      [0, 0, 1, 1, 0, 22, -2, 1]])
        c = np.array([2, 1, -2, -1, 4, -5, 5, 5])
        b = np.array([40, 107, 61])
        d_down_asterisk = [0, 0, 0, 0, 0, 0, 0, 0]
        d_up_asterisk = [3, 5, 5, 3, 4, 5, 6, 3]
        ds = DualSimplexMethod(A, c, b, d_down_asterisk, d_up_asterisk)
        self.assertEqual(([3, 5, 0, 1.8779, 2.7545, 3.0965, 6, 3], 49.6576), ds.solve())

    def test_case_four(self):
        A = np.array([[1, -3, 2, 0, 1, -1, 4, -1, 0],
                      [1, -1, 6, 1, 0, -2, 2, 2, 2],
                      [2, 2, -1, 1, 0, -3, 8, -1, 1],
                      [4, 1, 0, 0, 1, -1, 0, -1, 1],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1]])
        c = np.array([-1, 5, -2, 4, 3, 1, 2, 8, 3])
        b = np.array([3, 9, 9, 5, 9])
        d_down_asterisk = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        d_up_asterisk = [5, 5, 5, 5, 5, 5, 5, 5, 5]
        ds = DualSimplexMethod(A, c, b, d_down_asterisk, d_up_asterisk)
        self.assertEqual(([1.1579, 0.6942, 0, 0, 2.8797, 0, 1.0627, 3.2055, 0], 38.7216), ds.solve())

    def test_case_five(self):
        A = np.array([[1, 7, 2, 0, 1, -1, 4],
                      [0, 5, 6, 1, 0, -3, -2],
                      [3, 2, 2, 1, 1, 1, 5]])
        c = np.array([1, 2, 1, -3, 3, 1, 0])
        b = np.array([1, 4, 7])
        d_down_asterisk = [-1, 1, -2, 0, 1, 2, 4]
        d_up_asterisk = [3, 2, 2, 5, 3, 4, 5]
        ds = DualSimplexMethod(A, c, b, d_down_asterisk, d_up_asterisk)
        self.assertEqual(None, ds.solve())

    def test_case_six(self):
        A = np.array([[2, -1, 1, 0, 0, -1, 3],
                      [0, 4, -1, 2, 3, -2, 2],
                      [3, 1, 0, 1, 0, 1, 4]])
        c = np.array([0, 1, 2, 1, -3, 4, 7])
        b = np.array([1.5, 9, 2])
        d_down_asterisk = [0, 0, -3, 0, -1, 1, 0]
        d_up_asterisk = [3, 3, 4, 7, 5, 3, 2]
        ds = DualSimplexMethod(A, c, b, d_down_asterisk, d_up_asterisk)
        self.assertEqual(([0, 1, 3.5, 0, 3.5, 1, 0], 1.5), ds.solve())

    def test_case_seven(self):
        A = np.array([[2, 1, 0, 3, -1, -1],
                      [0, 1, -2, 1, 0, 3],
                      [3, 0, 1, 1, 1, 1]])
        c = np.array([0, -1, 1, 0, 4, 3])
        b = np.array([2, 2, 5])
        d_down_asterisk = [2, 0, -1, -3, 2, 1]
        d_up_asterisk = [7, 3, 2, 3, 4, 5]
        ds = DualSimplexMethod(A, c, b, d_down_asterisk, d_up_asterisk)
        self.assertEqual(None, ds.solve())

    def test_case_eight(self):
        A = np.array([[1, 3, 1, -1, 0, -3, 2, 1],
                      [2, 1, 3, -1, 1, 4, 1, 1],
                      [-1, 0, 2, -2, 2, 1, 1, 1]])
        c = np.array([2, -1, 2, 3, -2, 3, 4, 1])
        b = np.array([4, 12, 4])
        d_down_asterisk = [-1, -1, -1, -1, -1, -1, -1, -1]
        d_up_asterisk = [2, 3, 1, 4, 3, 2, 4, 4]
        ds = DualSimplexMethod(A, c, b, d_down_asterisk, d_up_asterisk)
        self.assertEqual(([-1, 0.4074, 1, 4, -0.3704, 1.7407, 4, 4], 37.5555), ds.solve())


if __name__ == '__main__':
    unittest.main()
