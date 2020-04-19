import matplotlib.pyplot as plt
import numpy as np
import cv2

def edgedetect (channel):
    sobelX = cv2.Sobel(channel, cv2.CV_16S, 1, 0)
    sobelY = cv2.Sobel(channel, cv2.CV_16S, 0, 1)
    sobel = np.hypot(sobelX, sobelY)

    sobel[sobel > 255] = 255; # Some values seem to go above 255. However RGB channels has to be within 0-255
    return sobel

def confidenceMap(sgmf, name):
    ## (1) read and extract the blue channel
    img = cv2.imread(sgmf)
    # uncomment for pre-blurring
#    img = cv2.medianBlur(img,5)
    red = img[:,:,1]
    green = img[:,:,2]

    # Adaptive Thresholding
    green2 = cv2.adaptiveThreshold(green, 255,
                                        cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY, 3, 2)

    red2 = cv2.adaptiveThreshold(red, 255,
                                        cv2.ADAPTIVE_THRESH_MEAN_C,
                                        cv2.THRESH_BINARY, 3, 2)

    edgeImgG = np.max( np.array([ edgedetect(red2) ]), axis=0 )
    edgeImgR = np.max( np.array([ edgedetect(green2) ]), axis=0 )

    edgeImgR[edgeImgR <= np.mean(edgeImgR)] = 0;
    edgeImgG[edgeImgG <= np.mean(edgeImgG)] = 0;

    # Blur the image
    # changer le (21,21)PG en (7,7)AV
    maskimg = cv2.GaussianBlur(edgeImgG,(7,7),0)*cv2.GaussianBlur(edgeImgR,(7,7),0)

    maskimg = 255 - maskimg * 255
    cv2.imwrite(name, maskimg)




confidenceMap('./data/miroir_plan/cam_match_AV.png', './data/miroir_plan/quadrupleconf_AV.png')
