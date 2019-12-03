
import cv2
import numpy as np
from skimage.io import imsave, imread

####################################################
####################################################

for i in range(24):

    scan = imread("scan/img{:04d}.png".format(i))

    #cv2.convertScaleAbs(scan, scan, 1./255., 0)

    #scan = np.uint16(scan)

    #cv2.imwrite("ThScan/img{:04d}.png".format(i), scan, [int(cv2.IMWRITE_PNG_COMPRESSION), 6])
    imsave("ThScan/img{:04d}.png".format(i),scan)


#####################################################
#####################################################

scan = cv2.imread("scan/img0000.png")

print(scan.dtype)
print(scan.shape)

ThScan = cv2.imread("ThScan/img0000.png")

print(ThScan.dtype)
print(ThScan.shape)




