import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2
from skimage.io import imread, imsave
import seaborn as sns

from Camera import Camera
from Ecran import Ecran
from nc import *
from util import *

# Setup
w = np.array( [1600, 900] ) #pixels
W = w * 0.277e-3 #m
ecran = Ecran( W, w)
########################################################


###################
# Camera Point Grey

K1 = np.transpose( np.array([[1.045060e+04 , 0., 0.],
             [0., 1.045055e+04, 0.],
             [1.604034e+03, 1.360889e+03 , 1.]]) )


R1 = np.array([[-9.840379e-01 , -4.342395e-02, -1.725799e-01],
             [1.089694e-01 , 6.196762e-01 , -7.772561e-01 ],
             [1.406952e-01 , -7.836554e-01 , -6.050530e-01 ]])

####### unitaire ok

T1 = np.array([-7.493951e+01, -2.746327e+02, 5.359261e+02])*1e-3


w1 = np.array( [3376, 2704] )
W1 = w * 1.69e-6

sgmf1 = "13mars/lentille_plano_convexe/cam_match_PG.png"
mask1 = "jc_menage/conf_PG.png"

cam1 = Camera(ecran, K1, R1, T1, W1, w1, sgmf1, mask1)
cam1.centre_x=1768; cam1.centre_y=1283; cam1.rayon=1300

####################
# Camera Allied Vision

K2 = np.transpose( np.array([[1.961112e+03, 0., 0.],
             [0., 1.960235e+03, 0.],
             [3.910473e+02 , 2.925270e+02, 1.]]) )

R2 = np.array([[-9.809168e-01 , -2.576017e-02, -1.927140e-01],
             [1.590671e-01, -6.762932e-01, -7.192532e-01],
             [-1.118031e-01, -7.361820e-01, 6.674849e-01]])

####### unitaire ok

T2 = np.array([-1.134723e+01, -4.128016e+02, 1.099632e+02])*1e-3


w2 = np.array( [780, 580] )
W2 = w * 8.3e-6
sgmf2 = "13mars/lentille_plano_convexe/cam_match_AV.png"
mask2 = "jc_menage/conf_AV.png"

cam2 = Camera(ecran, K2, R2, T2, W2, w2, sgmf2, mask2)
cam2.centre_x=308; cam2.centre_y=235; cam2.rayon=245
