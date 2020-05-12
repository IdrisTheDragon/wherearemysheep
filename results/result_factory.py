import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from finders import Templating, Thresholding
from imageManager import ImageManager
import cv2
import numpy as np

from tifffile import TiffFile

def tifToPNG():
    for x in range(1,9):
        with TiffFile("images/image-{0}.tif".format(x)) as tif:
            image = tif.asarray()
            r = image[:, :, 0]
            g = image[:, :, 1]
            b = image[:, :, 2]
            outlined = cv2.merge((r, g, b))
            cv2.imwrite("images/image-{0}.png".format(x),outlined)


def threshold(filename):
    m = Thresholding(threshold_value=180,min_width_height=4)
    s: ImageManager = ImageManager(filename)
    sheeps = []
    for x in range(0,255,20):
        m.threshold_value = x
        s.singleLayerFind(m, 0)
        s.saveIntermidiary('images/threshold/{0}-t-image-1.tif'.format(x))
        s.outline_mammal(baseImage='rgb')
        s.saveOutlined('images/threshold/{0}-o-image-1.png'.format(x))
        sheeps.append(len(s.locations))
    print(sheeps)

def getSplit():
    with TiffFile("images/image-4.tif") as tif:
        image = tif.asarray()
        r = image[:, :, 0]
        g = image[:, :, 1]
        b = image[:, :, 2]
        re = image[:, :, 3]
        ni = image[:, :, 4]

        split = {'red':r,'green':g,'blue':b,'rededge':re,'nearir':ni}
    return split

def colourBandComparison():
    split = getSplit()
    for name,image in split.items():
        print(name,image.shape)
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        fig: plt.Figure = plt.figure()
        fig.suptitle(name)
        ax: Axes3D = fig.add_subplot(111, projection='3d')
        x = range(image.shape[0])
        y = range(image.shape[1])
        X, Y = np.meshgrid(x, y)
        ax.plot_surface(X.T, Y.T, image)
        plt.savefig('images/image-4-{0}.png'.format(name))

def colourBandCombiner():
    s: ImageManager = ImageManager('images/image-4.tif')
    image = s.combineToSingleLayer([0.2,0.2,0.2,-0.2,-0.2])
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    fig: plt.Figure = plt.figure()
    fig.suptitle('Combined')
    ax: Axes3D = fig.add_subplot(111, projection='3d')
    x = range(image.shape[0])
    y = range(image.shape[1])
    print(image.shape)
    X, Y = np.meshgrid(x, y)
    ax.plot_surface(X.T, Y.T, image)
    plt.savefig('images/image-4-combined.png')

    s: ImageManager = ImageManager('images/image-4.tif')
    image = s.combineToSingleLayer([0.2, 0.2, 0.2, -0.2, -0.2])
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    row = image[4]
    #print(row)
    sum = 0
    for x in row:
        sum = sum + x
    backav = sum / len(row)
    print('background', backav)

    sheep = image[27, 25:39]
    #print(sheep)
    sum = 0
    for x in sheep:
        sum = sum + x
    sheepav = sum / len(sheep)
    print('sheep', sheepav)

    print('dif', sheepav - backav)

def getSamples():
    split = getSplit()
    for name, image in split.items():

        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        row = image[4]
        print(name)
        #print(row)
        sum = 0
        for x in row:
            sum = sum + x
        backav = sum / len(row)
        print('background', backav)

        sheep = image[27, 25:39]
        #print(sheep)
        sum = 0
        for x in sheep:
            sum = sum + x
        sheepav = sum / len(sheep)
        print('sheep', sheepav)

        print('dif', sheepav - backav)


if __name__ == '__main__':
    # threshold('images/image-1.tif')
    # threshold('images/image-2.tif')
    # threshold('images/image-3.tif')
    # threshold('images/image-4.tif')
    # threshold('images/image-5.tif')
    # threshold('images/image-6.tif')
    # threshold('images/image-7.tif')
    # threshold('images/image-8.tif')
    # tifToPNG()
    #colourBandComparison()
    getSamples()
    colourBandCombiner()