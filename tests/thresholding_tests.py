import unittest

from finders import thresholding
import cv2


class ThresholdingTests(unittest.TestCase):
    def test_first_image(self):
        img = cv2.imread("images/image.TIF", cv2.IMREAD_UNCHANGED)
        img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        locations, threshold_img = thresholding.wheresmysheep_threshold(img, threshold_value=120, min_pixels_in_sheep=10)
        self.assertEqual(10,len(locations))

    def test_second_image(self):
        img = cv2.imread("images/image2.JPG", cv2.IMREAD_UNCHANGED)
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        locations, threshold_img = thresholding.wheresmysheep_threshold(img_gray, threshold_value=230, min_pixels_in_sheep=50)
        self.assertEqual(5,len(locations))


if __name__ == '__main__':
    unittest.main()
