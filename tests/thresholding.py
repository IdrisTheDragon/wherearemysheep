import unittest

import thresholding


class MyTestCase(unittest.TestCase):
    def test_something(self):
        thresholding.wheresmysheep_threshold("images/image.TIF")
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
