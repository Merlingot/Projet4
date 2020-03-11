import numpy as np
import cv2
from skimage.io import imread, imsave


for i in range(24):
    
    src    = imread("scan_3channels/dstFringes_{:03d}.png".format(i))

    print("fringes_{:03d}.png".format(i) + "-->" + "dstFringes_{:03}.png".format(i)) 

    src = np.mean(src, axis=2)

    imsave("scan/dstFringes_{:03d}.png".format(i), src, format='png')

    #cv2.waitKey(0)


