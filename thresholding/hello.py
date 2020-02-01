import math

import cv2  # OpenCV
import numpy as np  # Arrays (1D, 2D, and matrices)
import matplotlib.pyplot as plt  # Plot

threshold_value = 120
min_pixels_in_sheep = 10
rectangle_size = 30
negative_offset = 10


def main():
    """Main algorithm for this attempt using thresholding"""

    # load the image and convert to grayscale
    img = cv2.imread("image.TIF")
    print(img.shape)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # do a binary threshold on the image based on provided variables above
    threshold_img = threshold(img_gray)
    cv2.imwrite("threshold.png", threshold_img)
    print(threshold_img.shape)

    # locate the none zero pixels and group neighbouring to find the sheep locations
    locations = sheep_locations(threshold_img)
    print(locations)
    print(len(locations))

    # outline sheep in original image and save
    identified_sheep_img = outline_sheep(img, locations)
    cv2.imwrite("identified_sheep_img.png", identified_sheep_img)


def threshold(img):
    """Threshold the image based on values at top of script"""
    _, threshold_img = cv2.threshold(img, threshold_value, 255, cv2.THRESH_BINARY)

    return threshold_img


def sheep_locations(image):
    """ find the sheep coordinates, based on the none zero pixels groupings"""
    coords = []

    # for each none zero pixels
    for row in range(image.shape[0]):
        for column in range(image.shape[1]):
            if image[row, column] > 0:
                # find and eliminate neighbours, making note of how many.
                count, image = expand_remove(row, column, image)
                # if there are a certain number in a group it is probably a sheep so save the coordinates
                if count > min_pixels_in_sheep:
                    coords.append([row, column, count])
    return coords


def expand_remove(row, column, image):
    """find none zero neighbours of a point in a grid"""

    count = 0
    queue = {(row, column)}  # setup a set of coordinates ready to check
    checked = {0}  # setup a set to store our checked coords to save duplication
    while len(queue) > 0:
        coord = queue.pop()
        if coord not in checked:
            checked.add(coord)
            # is coord inside image and it none zero
            if 0 < coord[0] < image.shape[0] and 0 < coord[1] < image.shape[1] and image[coord[0], coord[1]] > 0:
                # count the pixel and remove it from image
                count = count + 1
                image[coord[0], coord[1]] = 0
                # add its neighbours to queue ready to check
                queue.add((coord[0] + 1, coord[1]))
                queue.add((coord[0] - 1, coord[1]))
                queue.add((coord[0], coord[1] + 1))
                queue.add((coord[0], coord[1] - 1))
    return count, image


def outline_sheep(image, coords):
    """based on coordinates provided outline the sheep in the image"""
    identified_sheep_image = image
    for location in coords:
        identified_sheep_image = cv2.rectangle(
            identified_sheep_image,
            (location[1] - negative_offset, location[0] - negative_offset),
            (location[1] + rectangle_size, location[0] + rectangle_size),
            (0, 0, 255),
            3
        )
    return identified_sheep_image


if __name__ == '__main__':
    main()
