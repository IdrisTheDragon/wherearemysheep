import thresholding

import cv2
import numpy as np
from libtiff import TIFF, TIFFfile, TIFFimage
from tifffile import TiffFile, TiffWriter, TiffTag
import outline


def three_channel_file():
    """Main algorithm for this attempt using thresholding"""
    # load the image and convert to grayscale
    img = cv2.imread("images/image2.JPG", cv2.IMREAD_UNCHANGED)
    print(img.shape)
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    locations, threshold_img = thresholding.wheresmysheep_threshold(img_gray, threshold_value=230,
                                                                    min_pixels_in_sheep=50)

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
    locations, threshold_img = thresholding.wheresmysheep_threshold(img, threshold_value=120, min_pixels_in_sheep=10)

    # outline sheep in original image and save
    identified_sheep_img = outline.outline_sheep(img, locations)
    cv2.imwrite("images/result/image.png", identified_sheep_img)
    return locations, identified_sheep_img, threshold_img


# a change
def large_file():
    tif = TIFF.open('images/image3.tif', mode='r')
    images = tif.read_image()
    print(images.shape)
    image = images[:, :, 0]
    print(image.shape)
    print(image)
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    print(image)
    locations, threshold_img = thresholding.wheresmysheep_threshold(image, threshold_value=200, min_pixels_in_sheep=15)

    identified_sheep_img = outline.outline_sheep(image, locations)
    cv2.imwrite("images/result/identified_sheep_img.png", identified_sheep_img)

def fileInfo(tif:TiffFile):
    print(tif.flags)
    print(tif.geotiff_metadata)
    for page in tif.pages:
        print(page.tags)
        print(page.geotiff_tags)
        print(page.shape)
        print(page.dtype)
        print(page.flags)

def metadataGeoTags(tif):
    geoTag: TiffTag = tif.pages[0].tags.get('GeoKeyDirectoryTag')
    g: TiffTag = tif.pages[0].tags.get(34737)
    g2: TiffTag = tif.pages[0].tags.get(34736)
    g3: TiffTag = tif.pages[0].tags.get(33922)
    g4: TiffTag = tif.pages[0].tags.get(33550)

    tags = [(geoTag.code, 'H', geoTag.count, geoTag.value),
            (g.code, 's', g.count, g.value),
            (g2.code, 'd', g2.count, g2.value),
            (g3.code, 'd', g3.count, g3.value),
            (g4.code, 'd', g4.count, g4.value)]
    return tags

    # tif = TIFF.open('images/image3.tif', mode='r')
    # images = tif.read_image()
    # print(images.shape)
    # image = images[:, :, 0]
    # print(image.shape)
    # print(image)
    # image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    # print(image)
    # locations, threshold_img = thresholding.wheresmysheep_threshold(image, threshold_value=200, min_pixels_in_sheep=15)
    #
    # identified_sheep_img = outline.outline_sheep(image, locations)
    # cv2.imwrite("images/result/identified_sheep_img.png", identified_sheep_img)

def tif_process():
    with TiffFile('images/image3.tif') as tif:
        #fileInfo(tif)
        tags = metadataGeoTags(tif)
        image = tif.asarray()
        print(image.shape)
        sample = image[:, :, 0]
        image = cv2.normalize(sample, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        locations, threshold_img = thresholding.wheresmysheep_threshold(image, threshold_value=200,
                                                                          min_pixels_in_sheep=15)
        blank_image = np.zeros(threshold_img.shape)
        identified_sheep_img = outline.outline_sheep(blank_image, locations)

        with TiffWriter('images/threshold.tif', bigtiff=True) as tifw:
            tifw.save(threshold_img,extratags=tags)
        with TiffWriter('images/outline.tif', bigtiff=True) as tifw:
            tifw.save(identified_sheep_img, extratags=tags)


    with TiffFile('images/threshold.tif') as tif:
        #fileInfo(tif)
        pass


if __name__ == '__main__':
    tif_process()
