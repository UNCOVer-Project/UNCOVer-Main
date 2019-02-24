import cv2
import numpy as np

img_path = input('Image path: ')
img = cv2.imread(img_path)
cv2.imshow('image', img)
cv2.waitKey()