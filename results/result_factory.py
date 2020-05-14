import os

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

def generateTemplates():
    for templateSize in range(10,50,10):
        for sheepSize in range(5,int(templateSize/2)+1,5):
            template = np.full((templateSize, templateSize), 0, dtype=np.uint8)
            template = cv2.circle(template, (int(templateSize/2), int(templateSize/2)), sheepSize, 255, cv2.FILLED)
            cv2.imwrite('images/templates/template-{0}-{1}-{2}.png'.format(templateSize, sheepSize, 'circle'), template)
            template = np.full((templateSize, templateSize), 0, dtype=np.uint8)
            template = cv2.ellipse(img=template, center=(int(templateSize / 2), int(templateSize / 2)), axes=(int(sheepSize/2), sheepSize),
                                   angle=90, startAngle=0, endAngle=360, color=255, thickness=cv2.FILLED)
            cv2.imwrite('images/templates/template-{0}-{1}-{2}.png'.format(templateSize, sheepSize, 'ellipse'), template)

def testTempaltes(filename):
    sheeps = []
    s: ImageManager = ImageManager(filename)
    order = []
    for file in os.listdir('images/templates'):
        print(file)
        template = cv2.imread('images/templates/' + file,cv2.IMREAD_GRAYSCALE)
        m = Templating(template, 0.50)
        s.singleLayerFind(m, 0)
        s.saveIntermidiary('images/template-results/{0}-t-image-1.tif'.format(file))
        s.outline_mammal(baseImage='rgb')
        s.saveOutlined('images/template-results/{0}'.format(file))
        sheeps.append(len(s.locations))
        order.append(file)
    for x in sheeps:
        print(x)
    for x in order:
        print(x)

def testExtraTemplates(filename):
    sheeps = []
    order = []
    template = cv2.imread(filename, cv2.IMREAD_GRAYSCALE)
    print(template.shape)
    m = Templating(template, 0.90)
    for x in range(1,9):
        s: ImageManager = ImageManager('images/image-{0}.tif'.format(x))
        s.singleLayerFind(m, 0)
        s.saveIntermidiary('images/template-results2/{0}.tif'.format(x))
        s.outline_mammal(baseImage='rgb')
        s.saveOutlined('images/template-results2/{0}'.format(x))
        sheeps.append(len(s.locations))
        order.append(x)

    for x in sheeps:
        print(x)
    for x in order:
        print(x)


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
    #getSamples()
    #colourBandCombiner()
    #generateTemplates()
    #testTempaltes('images/image-1.tif')
    #testTempaltes('images/image-2.tif')
    #testTempaltes('images/image-3.tif')
    #testTempaltes('images/image-4.tif')
    #testTempaltes('images/image-5.tif')
    #testTempaltes('images/image-6.tif')
    #testTempaltes('images/image-7.tif')
    testTempaltes('images/image-8.tif')
    #testExtraTemplates('images/image-4.png')
    #testExtraTemplates('images/sheep_(839, 3432).tif')
    #testExtraTemplates('images/image-4-crop.png')