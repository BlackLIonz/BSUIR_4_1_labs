import unittest
import numpy as np
from SAIO.lab2.branch_and_border_method import BranchBorderMethod


class TestDualSimplexMethod(unittest.TestCase):

    def test_case_example_one(self):
        A = np.array([[1, -5, 3, 1, 0, 0],
                      [4, -1, 1, 0, 1, 0],
                      [2, 4, 2, 0, 0, 1]])
        b = np.array([-8, 22, 30])
        c = np.array([7, -2, 6, 0, 5, 2])
        d_down = np.array([2, 1, 0, 0, 1, 1])
        d_up = np.array([6, 6, 5, 2, 4, 6])
        bb = BranchBorderMethod(A, c, b, d_down, d_up)
        self.assertEqual(([6, 3, 0, 1, 1, 6], 53), bb.solve())

    def test_case_example_two(self):
        A = np.array([[1, 0, 3, 1, 0, 0],
                      [0, -1, 1, 1, 1, 2],
                      [-2, 4, 2, 0, 0, 1]])
        b = np.array([10, 8, 10])
        c = np.array([7, -2, 6, 0, 5, 2])
        d_down = np.array([0, 1, -1, 0, -2, 1])
        d_up = np.array([3, 3, 6, 2, 4, 6])
        bb = BranchBorderMethod(A, c, b, d_down, d_up)
        self.assertEqual(([1, 1, 3, 0, 2, 2], 37), bb.solve())

    def test_case_example_three(self):
        A = np.array([[1, 0, 1, 0, 0, 1],
                      [1, 2, -1, 1, 1, 2],
                      [-2, 4, 1, 0, 1, 0]])
        b = np.array([-3, 3, 13])
        c = np.array([-3, 2, 0, -2, -5, 2])
        d_down = np.array([-2, -1, -2, 0, 1, -4])
        d_up = np.array([2, 3, 1, 5, 4, -1])
        bb = BranchBorderMethod(A, c, b, d_down, d_up)
        self.assertEqual(([-2, 2, 0, 2, 1, -1], -1), bb.solve())

    def test_case_one(self):
        A = np.array([[1, 0, 0, 12, 1, -3, 4, -1],
                      [0, 1, 0, 11, 12, 3, 5, 3],
                      [0, 0, 1, 1, 0, 22, -2, 1]])
        c = np.array([2, 1, -2, -1, 4, -5, 5, 5])
        b = np.array([40, 107, 61])
        d_down = [0, 0, 0, 0, 0, 0, 0, 0]
        d_up = [3, 5, 5, 3, 4, 5, 6, 3]
        bb = BranchBorderMethod(A, c, b, d_down, d_up)
        self.assertEqual(([1, 1, 2, 2, 3, 3, 6, 3], 39), bb.solve())

    def test_case_two(self):
        A = np.array([[1, -3, 2, 0, 1, -1, 4, -1, 0],
                      [1, -1, 6, 1, 0, -2, 2, 2, 0],
                      [2, 2, -1, 1, 0, -3, 8, -1, 1],
                      [4, 1, 0, 0, 1, -1, 0, -1, 1],
                      [1, 1, 1, 1, 1, 1, 1, 1, 1]])
        c = np.array([-1, 5, -2, 4, 3, 1, 2, 8, 3])
        b = np.array([3, 9, 9, 5, 9])
        d_down = [0, 0, 0, 0, 0, 0, 0, 0, 0]
        d_up = [5, 5, 5, 5, 5, 5, 5, 5, 5]
        bb = BranchBorderMethod(A, c, b, d_down, d_up)
        self.assertEqual(([1, 1, 1, 1, 1, 1, 1, 1, 1], 23), bb.solve())

    def test_case_three(self):
        A = np.array([[1, 0, 0, 12, 1, -3, 4, -1, 2.5, 3],
                      [0, 1, 0, 11, 12, 3, 5, 3, 4, 5.1],
                      [0, 0, 1, 1, 0, 22, -2, 1, 6.1, 7]])
        c = np.array([2, 1, -2, -1, 4, -5, 5, 5, 1, 2])
        b = np.array([43.5, 107.3, 106.3])
        d_down = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        d_up = [2, 4, 5, 3, 4, 5, 4, 4, 5, 6]
        bb = BranchBorderMethod(A, c, b, d_down, d_up)
        self.assertEqual(([1, 1, 2, 2, 2, 3, 3, 3, 3, 3], 29), bb.solve())

    def test_case_four(self):
        A = np.array([[4, 0, 0, 0, 0, -3, 4, -1, 2, 3],
                      [0, 1, 0, 0, 0, 3, 5, 3, 4, 5],
                      [0, 0, 1, 0, 0, 22, -2, 1, 6, 7],
                      [0, 0, 0, 1, 0, 6, -2, 7, 5, 6],
                      [0, 0, 0, 0, 1, 5, 5, 1, 6, 7],
                      ])
        c = np.array([2, 1, -2, -1, 4, -5, 5, 5, 1, 2])
        b = np.array([8, 5, 4, 7, 8])
        d_down = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        d_up = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        bb = BranchBorderMethod(A, c, b, d_down, d_up)
        self.assertEqual(([2, 5, 4, 7, 8, 0, 0, 0, 0, 0], 26), bb.solve())


if __name__ == '__main__':
    unittest.main()
