from thresholding import Thresholding

import cv2

if __name__ == '__main__':
    t = Thresholding()
    _, image_wsheep, _ = t.wheresmysheep_threshold("images/image.TIF")
    cv2.imwrite("images/result/image.png", image_wsheep)
    t = Thresholding(threshold_value=230,min_pixels_in_sheep=50,rectangle_size=70)
    _,image_wsheep, _ = t.wheresmysheep_threshold("images/image2.JPG")
    cv2.imwrite("images/result/image2.png",image_wsheep)
