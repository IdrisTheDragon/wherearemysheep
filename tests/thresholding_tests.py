import unittest

from thresholding import Thresholding


class ThresholdingTests(unittest.TestCase):
    def test_first_image(self):
        t = Thresholding(
            threshold_value=120,
            min_pixels_in_sheep=10,
            rectangle_size=30)
        locations, _, _ = t.wheresmysheep_threshold("images/image.TIF")
        self.assertEqual(len(locations), 10)

    def test_second_image(self):
        t = Thresholding(
            threshold_value=230,
            min_pixels_in_sheep=50,
            rectangle_size=70)
        locations, _, _ = t.wheresmysheep_threshold("images/image2.JPG")
        self.assertEqual(len(locations), 5)


if __name__ == '__main__':
    unittest.main()
