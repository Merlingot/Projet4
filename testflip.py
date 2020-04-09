import numpy as np
import cv2 as cv
import glob
import matplotlib.pyplot as plt

fname='./allo.jpg'
img = cv.imread(fname)
img = cv.resize(img, (960, 540))
img = cv.flip(img, 1)

cv.imshow('img', img)
cv.waitKey(0)
