import numpy as np
import cv2
from skimage.io import imread, imsave


for i in range(24):
    
    srcAV    = imread("scan_AV_3channels/dstFringes_{:03d}.png".format(i))
    srcPG    = imread("scan_PG_3channels/dstFringes_{:03d}.png".format(i))

    print("fringes_{:03d}.png".format(i) + "-->" + "dstFringes_{:03}.png".format(i)) 

    srcAV = np.mean(srcAV, axis=2).astype(np.uint8)
    srcPG = np.mean(srcPG, axis=2).astype(np.uint8)

    imsave("scan_AV/dstFringes_{:03d}.png".format(i), srcAV, format='png')
    imsave("scan_PG/dstFringes_{:03d}.png".format(i), srcPG, format='png')



