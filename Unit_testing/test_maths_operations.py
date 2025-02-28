from Mathematical_operations import MathsOperations
import unittest

class TestMathOperations(unittest.TestCase):

    def setUp(self):
        self.obj = MathsOperations()

    def test_addition(self):
        self.assertAlmostEqual(self.obj.add(3, 4), 7)

    def test_multiplication(self):
        self.assertAlmostEqual(self.obj.multiply(3, 4), 12)

    def test_addition_invalid_type(self):
        with self.assertRaises(TypeError):
            self.obj.add(3, "four")

    def test_multiplication_invalid_type(self):
        with self.assertRaises(TypeError):
            self.obj.multiply(3, [4])
        

if __name__ == "__main__":
    unittest.main()
