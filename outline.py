import cv2

extra=30


def outline_sheep(image, coords):
    """based on coordinates provided outline the sheep in the image"""
    for location in coords:
        center = location[0]
        size = location[2]

        image = cv2.rectangle(
            image,
            (center[1] - round(size[1]/2) - extra, center[0] - round(size[0]/2) - extra),
            (center[1] + round(size[1]/2) + extra, center[0] + round(size[0]/2) + extra),
            255,
            3
        )
    return image
