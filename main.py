from thresholding import Thresholding

import cv2
import numpy as np
from libtiff import TIFF
import outline


def three_channel_file():
    """Main algorithm for this attempt using thresholding"""
    # load the image and convert to grayscale
    img = cv2.imread("images/image2.JPG", cv2.IMREAD_UNCHANGED)
    print(img.shape)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    t = Thresholding(threshold_value=230, min_pixels_in_sheep=50)
    locations, threshold_img = t.wheresmysheep_threshold(img_gray)

    # outline sheep in original image and save
    identified_sheep_img = outline.outline_sheep(img, locations)
    cv2.imwrite("images/result/image2.png", identified_sheep_img)
    return locations, identified_sheep_img, threshold_img

def single_channel_small_tiff():
    img = cv2.imread("images/image.TIF", cv2.IMREAD_UNCHANGED)
    print(img.shape)
    print(img)
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    print(img)
    t = Thresholding(threshold_value=120, min_pixels_in_sheep=10)
    locations, threshold_img = t.wheresmysheep_threshold(img)

    # outline sheep in original image and save
    identified_sheep_img = outline.outline_sheep(img, locations)
    cv2.imwrite("images/result/image.png", identified_sheep_img)
    return locations, identified_sheep_img, threshold_img


def large_file():
    tif = TIFF.open('images/image3.tif', mode='r')
    images = tif.read_image()
    print(images.shape)
    image = images[:, :, 0]
    print(image.shape)
    print(image)
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    print(image)
    t = Thresholding(threshold_value=230)
    locations, threshold_img = t.wheresmysheep_threshold(image)

    identified_sheep_img = outline.outline_sheep(image, locations)
    cv2.imwrite("images/result/identified_sheep_img.png", identified_sheep_img)


if __name__ == '__main__':
    large_file()
