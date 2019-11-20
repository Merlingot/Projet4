import numpy as np
import cv2
from skimage.io import imread, imsave

distCoeff = np.zeros((8,1),np.float64)

# TODO: add your coefficients here!
k1 = 0.0;
k2 = 0.0;
p1 = 0.0;
p2 = 0.0;
k3 = 0.0;
k4 = 0.0;
k5 = 0.0;
k6 = 0.0;

distCoeff[0,0] = k1;
distCoeff[1,0] = k2;
distCoeff[2,0] = p1;
distCoeff[3,0] = p2;
distCoeff[4,0] = k3;
distCoeff[5,0] = k4;
distCoeff[6,0] = k5;
distCoeff[7,0] = k6;

#-Offset

x_off = 50
y_off = x_off
x_in = 50
y_in = x_in


for i in range(24):
    
    src    = imread("../fringes/fringes_{:03d}.png".format(i))
    print("fringes_{:03d}.png".format(i) + "-->" + "dstFringes_{:03}.png".format(i)) 
    #-Define image caracteristics
    width  = src.shape[1]
    height = src.shape[0]

    #-Define camera caracteristics
    cam = np.eye(3,dtype=np.float32)
    cam[0,2] = width/2.0  # define center x
    cam[1,2] = height/2.0 # define center y
    cam[0,0] = 10.        # define focal length x
    cam[1,1] = 10.        # define focal length y

    dst = cv2.undistort(src,cam,distCoeff)
   
    #cv2.imshow('dst', dst)

    imsave("../thScan/dstFringes_{:03d}.png".format(i), dst)

    #cv2.waitKey(0)


