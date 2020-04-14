

import matplotlib.pyplot as plt
import numpy as np
import cv2

img=cv2.imread('./data/lentille_anto/cam_match_AV.png')

# Blur the image
img_0 = cv2.blur(img, ksize = (7, 7))
img_1 = cv2.GaussianBlur(img, ksize = (7, 7), sigmaX = 0)
img_2 = cv2.medianBlur(img, 7)
img_3 = cv2.bilateralFilter(img, 7, sigmaSpace = 75, sigmaColor =75)
# Plot the images
images = [img_0, img_1, img_2, img_3]
for p in images:
    plt.figure()
    plt.imshow(p)
    plt.show()
plt.show()
