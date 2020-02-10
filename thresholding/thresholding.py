import math

import cv2  # OpenCV
import numpy as np  # Arrays (1D, 2D, and matrices)
import matplotlib.pyplot as plt  # Plot
import sys


class Thresholding():
    """Everything to do with my thresholding attempt is contained in this class"""

    def __init__(
            self,
            threshold_value: int = 120,
            min_pixels_in_sheep: int = 10,):
        self.threshold_value = threshold_value
        self.min_pixels_in_sheep = min_pixels_in_sheep

    def wheresmysheep_threshold(
            self,
            image):
        # do a binary threshold on the image based on provided variables above
        threshold_img = self.threshold(image)
        cv2.imwrite("images/result/threshold.png", threshold_img)
        print(threshold_img.shape)
        print("locating sheep")

        # locate the none zero pixels and group neighbouring to find the sheep locations
        locations = self.sheep_locations(threshold_img)
        print(locations)
        print(len(locations))

        return locations, threshold_img


    def threshold(self, img):
        """Threshold the image based on values at top of script"""
        _, threshold_img = cv2.threshold(img, self.threshold_value, 255, cv2.THRESH_BINARY)

        return threshold_img

    def sheep_locations(self, image):
        """ find the sheep coordinates, based on the none zero pixels groupings"""
        coords = []

        # for each none zero pixels
        for row in range(image.shape[0]):
            sys.stdout.write('\r')
            sys.stdout.write(str(row) + "/" + str(image.shape[0]))
            sys.stdout.flush()
            for column in range(image.shape[1]):
                if image[row, column] > 0:
                    # find and eliminate neighbours, making note of how many.
                    count, image = self.expand_remove(row, column, image)
                    # if there are a certain number in a group it is probably a sheep so save the coordinates
                    if count > self.min_pixels_in_sheep:
                        coords.append([row, column, count])
        sys.stdout.write('\n')
        sys.stdout.flush()
        return coords

    def expand_remove(self, row, column, image):
        """find none zero neighbours of a point in a grid"""

        count = 0
        queue = {(row, column)}  # setup a set of coordinates ready to check
        checked = {0}  # setup a set to store our checked coords to save duplication
        while len(queue) > 0:
            coord = queue.pop()
            checked.add(coord)
            # is coord inside image and it none zero
            if 0 < coord[0] < image.shape[0] and 0 < coord[1] < image.shape[1] and image[coord[0], coord[1]] > 0:
                # count the pixel and remove it from image
                count = count + 1
                image[coord[0], coord[1]] = 0
                # add its neighbours to queue ready to check
                if (coord[0] + 1, coord[1]) not in checked:
                    queue.add((coord[0] + 1, coord[1]))
                if (coord[0] - 1, coord[1]) not in checked:
                    queue.add((coord[0] - 1, coord[1]))
                if (coord[0], coord[1] + 1) not in checked:
                    queue.add((coord[0], coord[1] + 1))
                if (coord[0], coord[1] - 1) not in checked:
                    queue.add((coord[0], coord[1] - 1))
        return count, image
