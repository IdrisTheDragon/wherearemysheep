import cv2

rectangle_size=70
negative_offset = 30

def outline_sheep(image, coords):
    """based on coordinates provided outline the sheep in the image"""
    identified_sheep_image = image
    for location in coords:
        identified_sheep_image = cv2.rectangle(
            identified_sheep_image,
            (location[1] - negative_offset, location[0] - negative_offset),
            (location[1] + rectangle_size, location[0] + rectangle_size),
            (0, 0, 255),
            3
        )
    return identified_sheep_image
