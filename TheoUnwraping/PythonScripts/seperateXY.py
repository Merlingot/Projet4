
import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage.io import imread, imsave
import seaborn as sns

#-Camera Parameters
x_res = 1000
y_res = 800

#-Importing cartography
cam = cv2.imread("../cam_match.png")

#-Green channel
g = cam.copy()
g[:,:,0] = 0
g[:,:,2] = 0

#-Blue channel
b = cam.copy()
b[:,:,0] = 0
b[:,:,1] = 0

cv2.imshow("Green channel", g)
cv2.imwrite("../cam_y.png", g)
cv2.waitKey(0)

cv2.imshow("Blue channel", b)
cv2.imwrite("../cam_x.png", b)
cv2.waitKey(0)

#-Pixel to Pixel cartography

cam = cam.astype('float64')

plt.figure()
axy = sns.heatmap(cam[:,:,1]*y_res/255, cmap="jet")

plt.figure()
axx = sns.heatmap(cam[:,:,2]*x_res/255, cmap="jet")

plt.show()


