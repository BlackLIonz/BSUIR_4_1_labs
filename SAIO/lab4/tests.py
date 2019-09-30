import unittest
import numpy as np

from SAIO.lab4.resource_allocation import ResourceAllocation


class TestResourceAllocation(unittest.TestCase):

    def test_case_one(self):
        table = np.array([[0, 1, 2, 2, 4, 5, 6],
                          [0, 2, 3, 5, 7, 7, 8],
                          [0, 2, 4, 5, 6, 7, 7]])
        bb = ResourceAllocation(table)
        self.assertEqual([0, 4, 2], bb.solve()[0])

    def test_case_two(self):
        table = np.array([[0, 1, 1, 3, 6, 10, 11],
                          [0, 2, 3, 5, 6, 7, 13],
                          [0, 1, 4, 4, 7, 8, 9]])
        bb = ResourceAllocation(table)
        self.assertEqual([0, 6, 0], bb.solve()[0])

    def test_case_three(self):
        table = np.array([[0, 1, 2, 4, 8, 9, 9, 23],
                          [0, 2, 4, 6, 6, 8, 10, 11],
                          [0, 3, 4, 7, 7, 8, 8, 24]])
        bb = ResourceAllocation(table)
        self.assertEqual([0, 0, 7], bb.solve()[0])

    def test_case_four(self):
        table = np.array([[0, 3, 3, 6, 7, 8, 9, 14],
                          [0, 2, 4, 4, 5, 6, 8, 13],
                          [0, 1, 1, 2, 3, 3, 10, 11]])
        bb = ResourceAllocation(table)
        self.assertEqual([7, 0, 0], bb.solve()[0])

    def test_case_five(self):
        table = np.array([[0, 2, 2, 3, 5, 8, 8, 10, 17],
                          [0, 1, 2, 5, 8, 10, 11, 13, 15],
                          [0, 4, 4, 5, 6, 7, 13, 14, 14],
                          [0, 1, 3, 6, 9, 10, 11, 14, 16]])
        bb = ResourceAllocation(table)
        self.assertEqual([0, 4, 1, 3], bb.solve()[0])

    def test_case_six(self):
        table = np.array([[0, 1, 3, 4, 5, 8, 9, 9, 11, 12, 12, 14],
                          [0, 1, 2, 3, 3, 3, 7, 12, 13, 14, 17, 19],
                          [0, 4, 4, 7, 7, 8, 12, 14, 14, 16, 18, 22],
                          [0, 5, 5, 5, 7, 9, 13, 13, 15, 15, 19, 24]])
        bb = ResourceAllocation(table)
        self.assertEqual([2, 7, 1, 1], bb.solve()[0])

    def test_case_seven(self):
        table = np.array([[0, 4, 4, 6, 9, 12, 12, 15, 16, 19, 19, 19],
                          [0, 1, 1, 1, 4, 7, 8, 8, 13, 13, 19, 20],
                          [0, 2, 5, 6, 7, 8, 9, 11, 11, 13, 13, 18],
                          [0, 1, 2, 4, 5, 7, 8, 8, 9, 9, 15, 19],
                          [0, 2, 5, 7, 8, 9, 10, 10, 11, 14, 17, 21]])
        bb = ResourceAllocation(table)
        self.assertEqual([7, 0, 2, 0, 2], bb.solve()[0])


if __name__ == '__main__':
    unittest.main()
