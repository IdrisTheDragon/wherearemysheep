import thresholding

from sheepfinder import MammalFinder


def three_channel_file():
    """Main algorithm for this attempt using thresholding"""

    m = thresholding.Thresholding(threshold_value=180)
    s: MammalFinder = MammalFinder("images/image2.JPG")
    s.find(m, 0)
    s.saveIntermidiary('images/result/threshold2.png')
    s.outline_sheep(baseImage='original')
    s.saveOutlined('images/result/outline2.png')


def single_channel_small_tiff():
    m = thresholding.Thresholding(threshold_value=120,min_pixels_in_sheep=10)
    s: MammalFinder = MammalFinder("images/image.TIF")
    s.find(m, 0)
    s.saveIntermidiary('images/result/threshold.tif')
    s.outline_sheep(baseImage='original')
    s.saveOutlined('images/result/outline.tif')

def large_file():
    m = thresholding.Thresholding(threshold_value=220)
    s: MammalFinder = MammalFinder("images/image3.tif")
    s.find(m,3)
    s.saveIntermidiary('images/threshold.tif')
    s.outline_sheep()
    s.saveOutlined('images/outline.tif')

if __name__ == '__main__':
    three_channel_file()

