from finders import Thresholding, Templating

from imageManager import ImageManager

import numpy as np
import cv2

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def three_channel_file_th():
    """Main algorithm for this attempt using thresholding"""

    m = Thresholding(threshold_value=180)
    s: ImageManager = ImageManager("images/image2.JPG")
    s.singleLayerFind(m, 0)
    s.saveIntermidiary('images/result/threshold2.png')
    s.outline_mammal(baseImage='original')
    s.saveOutlined('images/result/outline2.png')


def single_channel_small_tiff_th():
    m = Thresholding(threshold_value=120, min_pixels_in_sheep=10)
    s: ImageManager = ImageManager("images/image.TIF")
    s.singleLayerFind(m, 0)
    s.saveIntermidiary('images/result/threshold.tif')
    s.outline_mammal(baseImage='original')
    s.saveOutlined('images/result/outline.tif')

def large_file_th():
    m = Thresholding(threshold_value=220)
    s: ImageManager = ImageManager("images/image3.tif")
    s.singleLayerFind(m, 3)
    s.saveIntermidiary('images/threshold.tif')
    s.outline_mammal()
    s.saveOutlined('images/outline.tif')

def single_channel_small_tiff():
    template = np.zeros((30,30),dtype=np.uint8)
    template = cv2.circle(template,(15,15),10,255,cv2.FILLED)
    m = Templating(template,0.75)
    s: ImageManager = ImageManager("images/image.TIF")
    s.singleLayerFind(m, 0)
    s.saveIntermidiary('images/result/templating.tif')
    s.outline_mammal(baseImage='original')
    s.saveOutlined('images/result/outlinetemplating.tif')

def large_file():
    templateSize= 30
    template = np.full((templateSize, templateSize), 0 ,dtype=np.uint8)
    #template = cv2.circle(template, (15, 15), 7, 200, cv2.FILLED)
    template = cv2.circle(template, (int(templateSize/2), int(templateSize/2)), 5, 255, cv2.FILLED)
    #template = cv2.ellipse(img=template, center=(int(templateSize/2), int(templateSize/2)), axes=(4,8),angle=90,startAngle=0,endAngle=360,color=255,thickness=cv2.FILLED)
    cv2.imwrite('images/template.png',template)
    m = Templating(template,0.50)
    s: ImageManager = ImageManager("images/image3.tif")
    s.singleLayerFind(m, 1)
    #s.combinedSingleLayerFind(m,[0.299,0.587,0.114])
    #s.combinedSingleLayerFind(m, [0.2, 0.2, 0.2, 0.2, 0.2])
    #s.multiLayerFind(m)
    print(s.locations)
    s.saveIntermidiary('images/templating.tif')
    s.outline_mammal(padding=10)
    s.saveOutlined('images/outlinetemplating.tif')

def extracter():
    templateSize = 10
    template = np.full((templateSize, templateSize), 0, dtype=np.uint8)
    template = cv2.circle(template, (int(templateSize/2), int(templateSize/2)), 5, 255, cv2.FILLED)

    cv2.imwrite('images/template.png', template)
    m = Templating(template, 0.50)
    s: ImageManager = ImageManager("images/image3.tif")
    s.singleLayerFind(m, 0)
    s.extract_sheep("images/extracted")

def miniexample():
    template = cv2.imread("images/sheep_(839, 3432).png",cv2.IMREAD_GRAYSCALE)
    m = Templating(template, 0.82)
    s: ImageManager = ImageManager("images/sheeps.png")
    l,intermidary = s.combinedSingleLayerFind(m,[0.299,0.587,0.114])
    i = intermidary[:,:,1]
    cv2.imwrite("images/sheeps1.png",i)
    i = cv2.normalize(i, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    _,i = cv2.threshold(i,245,255,cv2.THRESH_BINARY)

    cv2.imwrite("images/sheeps2.png", i)

    s.outline_mammal("original")
    s.saveOutlined("images/sheeps3.png")


def analyser():
    image = cv2.imread('images/sheep_(839, 3432).tif',cv2.IMREAD_GRAYSCALE)
    image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    cv2.imwrite('images/sheep_(839, 3432).png',image)
    fig:plt.Figure = plt.figure()
    ax:Axes3D = fig.add_subplot(111,projection='3d')
    x = range(image.shape[0])
    y = range(image.shape[1])
    print(image.shape)
    X, Y = np.meshgrid(x, y)
    ax.plot_surface(X.T,Y.T,image)
    plt.savefig('images/sheep_(839, 3432)_graph.png')
    _,image = cv2.threshold(image,200,255,cv2.THRESH_BINARY)
    #image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
    fig: plt.Figure = plt.figure()
    ax: Axes3D = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X.T,Y.T,image)
    plt.savefig('images/sheep_(839, 3432)_graph1.png')


if __name__ == '__main__':
    #large_file_th()
    #single_channel_small_tiff()
    #extracter()
    analyser()
    #miniexample()
