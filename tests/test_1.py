import unittest

from math_model_v2 import Model_MLC

class TestModel(unittest.TestCase):
    def test_general_result(self):
        test_model = Model_MLC.math_model(150, 3300, 120, 1100, 14, 485, 111, "32ХГА", "rosniti_first")
        self.assertEqual(test_model[0], 1.87)


if __name__ == '__main__':
    unittest.main()