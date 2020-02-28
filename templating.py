import cv2  # OpenCV
import numpy as np  # Arrays (1D, 2D, and matrices)
import matplotlib.pyplot as plt  # Plot

from sheepfinder import  Finder

class templating(Finder):

    def __init__(self):
        self.template= None

    def findInImage(self,image):
        d = cv2.matchTemplate(image,self.template,cv2.TM_CCORR_NORMED)
        m,M,m_1,M_1 = cv2.minMaxLoc(d)
        print(m,M,m_1,M_1)