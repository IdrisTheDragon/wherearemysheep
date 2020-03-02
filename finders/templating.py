import cv2  # OpenCV

from finders.finder import Finder
from location import Location

import numpy as np


class Templating(Finder):

    def __init__(self,template=None,threshold=0.75):
        self.template= template
        self.threshold = threshold

    def findInImage(self,image):
        if image is None or len(image.shape) is not 2:
            print('error with image')
        image = cv2.normalize(image, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        m = np.float32([(1,0,self.template.shape[0]/2),(0,1,self.template.shape[1]/2)])
        d = cv2.matchTemplate(image,self.template,cv2.TM_CCORR_NORMED)
        d = cv2.warpAffine(d,m,dsize=(image.shape[1],image.shape[0]))

        m,M,m_1,M_1 = cv2.minMaxLoc(d)
        print(m,M,m_1,M_1)

        locations = []
        _,d2 = cv2.threshold(d, self.threshold, 1, cv2.THRESH_BINARY)
        d2 = cv2.normalize(d2, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        d = cv2.normalize(d, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
        contours, hier = cv2.findContours(d2, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            (x, y, w, h) = cv2.boundingRect(cnt)
            locations.append(Location((y,x),size=(h,w)))
        return locations, cv2.merge((d2,d,image))