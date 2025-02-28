from list_sum import *
import unittest


class test_sum_of_list_elements(unittest.TestCase):

    def setUp(self):
        self.obj = get_sum_elements()

    def test_sum(self):
        self.assertAlmostEqual(self.obj.get_sum(5,[1,2,3,4,5]),15)

    def test_sum_error(self): 
        with self.assertRaises(LengthError):
            self.obj.get_sum(5,[1,2,3,4])