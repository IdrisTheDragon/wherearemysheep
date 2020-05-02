import concurrent.futures
import sys
import time

import cv2  # OpenCV
import numpy as np  # Arrays (1D, 2D, and matrices)

from finders.finder import Finder
from location import Location


class Thresholding(Finder):

    def __init__(self,
                 threshold_value: int = 200,
                min_pixels_in_sheep: int = 10):
        self.threshold_value = threshold_value
        self.min_pixels_in_sheep = min_pixels_in_sheep

    def findInImage(self, image):
        print('doing the thing')
        if image is None or len(image.shape) is not 2:
            print('error with image')
        # do a binary threshold on the image based on provided variables above
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        _, threshold_img = cv2.threshold(image, self.threshold_value, 255, cv2.THRESH_BINARY)
        print(threshold_img.shape)
        print("locating sheep")

        locations = []
        contours, hier = cv2.findContours(threshold_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            if w > 5 and h> 5:
                locations.append(Location((y, x), size=(h, w)))
        print(locations)
        print(len(locations))
        return locations, threshold_img

        # locate the none zero pixels and group neighbouring to find the sheep locations
        #locations = self.__sheep_locations(threshold_img)
        #print(locations)
        #print(len(locations))

        #return locations, threshold_img

    def __sheep_locations(self, image):
        """ find the sheep coordinates, based on the none zero pixels groupings"""
        startTime = time.perf_counter()
        coords = []
        rows = image.shape[0]
        segSize = 50
        segments = round(rows / segSize)
        iterations = round(segments / 4)
        processedpixels = []

        with concurrent.futures.ProcessPoolExecutor() as executor:
            # first set
            args = ()
            offset = 0
            for itr in range(iterations):
                offset = itr * 4
                imageseg = image[offset * segSize:(offset + 4) * segSize]
                segstart = offset * segSize
                start = (offset + 1) * segSize
                end = (offset + 3) * segSize
                processedpixels.append((start, end))
                args = args + ([imageseg, self.min_pixels_in_sheep, segstart, start, end],)
            # end case
            offset = offset + 4
            imageseg = image[offset * segSize:min((offset + 4) * segSize, rows)]
            segstart = offset * segSize
            start = (offset + 1) * segSize
            end = min((offset + 3) * segSize, rows)
            processedpixels.append((start, end))
            args = args + ([imageseg, self.min_pixels_in_sheep, segstart, start, end],)

            image1 = np.empty((0, image.shape[1]))
            print("I just launched", len(args), "processess, lets wait for them to finish..")
            sys.stdout.write('\r' + str(0) + "/" + str(len(args)))
            sys.stdout.flush()
            for count, result in enumerate(executor.map(arghelper, args)):
                sys.stdout.write('\r' + str(count + 1) + "/" + str(len(args)))
                sys.stdout.flush()
                coords = coords + result[0]
                image1 = np.concatenate((image1, result[1]), axis=0)
            sys.stdout.write('\n')
            sys.stdout.flush()
            print()
            print("pixels done so far", processedpixels)
            print("Half done.. Found so far..", coords)
            print()

            # second set
            args = ()
            offset = 0
            # intial offset
            imageseg = image[0:2 * segSize]
            segstart = 0
            start = 0
            end = 1 * segSize
            processedpixels.append((start, end))
            args = args + ([imageseg, self.min_pixels_in_sheep, segstart, start, end],)
            # full cases
            for itr in range(iterations - 1):
                offset = (itr * 4) + 2
                imageseg = image[offset * segSize:(offset + 4) * segSize]
                segstart = offset * segSize
                start = (offset + 1) * segSize
                end = (offset + 3) * segSize
                processedpixels.append((start, end))
                args = args + ([imageseg, self.min_pixels_in_sheep, segstart, start, end],)
            # end caseAttributeError: Can't pickle local object
            offset = offset + 4
            segstart = offset * segSize
            segend = min((offset + 4) * segSize, rows)
            imageseg = image[segstart:segend]

            start = (offset + 1) * segSize
            end = min((offset + 3) * segSize, rows)
            processedpixels.append((start, end))
            args = args + ([imageseg, self.min_pixels_in_sheep, segstart, start, end],)

            print("oops I just launched another", len(args), "processess, lets wait for them to finish..")
            sys.stdout.write('\r' + str(0) + "/" + str(len(args)))
            sys.stdout.flush()
            for count, result in enumerate(executor.map(arghelper, args)):
                sys.stdout.write('\r' + str(count + 1) + "/" + str(len(args)))
                sys.stdout.flush()
                coords = coords + result[0]
            sys.stdout.write('\n')
            sys.stdout.flush()
            print("all pixels:", processedpixels)
            executor.shutdown()
        finish = time.perf_counter()
        print(f'Finished in {round(finish - startTime, 3)} second(s)')
        print()
        return coords


def arghelper(p):
    return sheep_locations_helper(*p)


def sheep_locations_helper(imageseg, min_pixels_in_sheep, segstart, start, end):
    coords = []

    # for each none zero pixels
    for row in range(start - segstart, end - segstart):
        # sys.stdout.write('\r')
        # sys.stdout.write(str(row) + "/" + str(imageseg.shape[0]))
        # sys.stdout.flush()
        for column in range(imageseg.shape[1]):
            if imageseg[row, column] > 0:
                # find and eliminate neighbours, making note of how many.
                count, imageseg, center, size = expand_remove(row, column, imageseg)
                # if there are a certain number in a group it is probably a sheep so save the coordinates
                max_pixels_in_sheep = 300
                if max_pixels_in_sheep > count > min_pixels_in_sheep:
                    l = Location((center[0] + segstart, center[1]),count,size)
                    coords.append(l)
    # sys.stdout.write('\n')
    # sys.stdout.flush()
    return coords, imageseg

def expand_remove(row, column, image):
    """find none zero neighbours of a point in a grid"""
    width = [row, row]
    height = [column, column]
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
            # track max width of sheep and adjust center
            if coord[0] < width[0]:
                width[0] = coord[0]
            elif width[1] < coord[0]:
                width[1] = coord[0]
            # track max height of sheep and adjust center
            if coord[1] < height[0]:
                height[0] = coord[1]
            elif height[1] < coord[1]:
                height[1] = coord[1]
            # add its neighbours to queue ready to check
            if (coord[0] + 1, coord[1]) not in checked:
                queue.add((coord[0] + 1, coord[1]))
            if (coord[0] - 1, coord[1]) not in checked:
                queue.add((coord[0] - 1, coord[1]))
            if (coord[0], coord[1] + 1) not in checked:
                queue.add((coord[0], coord[1] + 1))
            if (coord[0], coord[1] - 1) not in checked:
                queue.add((coord[0], coord[1] - 1))
    size = (width[1] - width[0], height[1] - height[0])
    center = (width[0]+round(size[0]/2),height[0]+round(size[1]/2))
    return count, image, center, size
