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
y_off = 400

#-Inset
x_in = 1 # ALWAYS >=1
y_in = x_in


for i in range(24):
    
    src    = imread("fringes/fringes_{:03d}.png".format(i))
    
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
   
    dst = cv2.resize(dst,(200,150))

    grey = imread("refImages/grey.png")
    grey[y_off+y_in:y_off+dst.shape[0]-y_in, x_off+x_in:x_off+dst.shape[1]-x_in] = dst[y_in:-y_in, x_in:-x_in]

    grey = cv2.resize(grey, (780,580))
    

    #cv2.imshow('grey', grey)

    imsave("thScan/dstFringes_{:03d}.png".format(i), grey)

    cv2.waitKey(0)


