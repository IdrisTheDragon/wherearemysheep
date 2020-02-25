import thresholding

import cv2
import numpy as np
from libtiff import TIFF,TIFFimage,TIFFfile,TiffChannelsAndFiles
import outline


def three_channel_file():
    """Main algorithm for this attempt using thresholding"""
    # load the image and convert to grayscale
    img = cv2.imread("images/image2.JPG", cv2.IMREAD_UNCHANGED)
    print(img.shape)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    locations, threshold_img = thresholding.wheresmysheep_threshold(img_gray,threshold_value=230, min_pixels_in_sheep=50)

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
    locations, threshold_img = thresholding.wheresmysheep_threshold(img,threshold_value=120, min_pixels_in_sheep=10)

    # outline sheep in original image and save
    identified_sheep_img = outline.outline_sheep(img, locations)
    cv2.imwrite("images/result/image.png", identified_sheep_img)
    return locations, identified_sheep_img, threshold_img

#a change
def large_file():
    tif = TIFF.open('images/image3.tif', mode='r')
    images = tif.read_image()
    print(images.shape)
    image = images[:, :, 0]
    print(image.shape)
    print(image)
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    print(image)
    locations, threshold_img = thresholding.wheresmysheep_threshold(image,threshold_value=200, min_pixels_in_sheep=15)

    identified_sheep_img = outline.outline_sheep(image, locations)
    cv2.imwrite("images/result/identified_sheep_img.png", identified_sheep_img)

def merge_large():
    tif = TIFF.open('images/image3.tif')
    #images = tif.read_image()
    #samples, sample_names = tif.get_samples()
    #print(sample_names)
    #print(samples)
    img = cv2.imread('images/result/threshold.png', cv2.IMREAD_GRAYSCALE)
    #print(images.shape)
    #print(img.shape)

    tif = TiffChannelsAndFiles(tif)
    t = tif.get_info()
    print()
    #????

    #print(images.shape)

    tif = TIFFimage(img)
    tif.write_file('images/merge.tif', compression='none')

if __name__ == '__main__':
    merge_large()
