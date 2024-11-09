import numpy as np
import cv2
import math

def nearestNeighboor(image, scale):
    img = cv2.imread(image)
    height, width, _ = img.shape
    resizedHeight = height * scale
    resizedWidth = width * scale
    resized = np.zeros((resizedHeight, resizedWidth, 3), np.uint8)

    RatioCol = height / resizedHeight
    RatioRow = width / resizedWidth

    for x in range(resizedWidth):
        for y in range(resizedHeight):
            resized[y,x] = img[math.ceil((y+1) * RatioCol) - 1, math.ceil((x+1) * RatioRow) - 1]
    return resized


