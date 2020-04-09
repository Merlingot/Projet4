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
import dataPG as pg
import dataAV as av

plt.close('all')

# Écran
# c =  (888,576)
c = (962,567)
w = np.array( [1600, 900] ) #pixels
W = w * 0.277e-3 #m
ecran = Ecran( W, w ,c )

#################################################################

# Camera Point Grey -------------------------------------
sgmf1 = "jc_menage/cam_match_PTG.png"
mask1 = "jc_menage/conf_PG.png"

K1 =  np.transpose(np.array([[pg.K11 , pg.K12, pg.K13],
             [pg.K21, pg.K22, pg.K23],
             [pg.K31, pg.K32, pg.K33]]))


R1 =  np.array([[pg.R11 , pg.R12, pg.R13],
             [pg.R21, pg.R22, pg.R23],
             [pg.R31, pg.R32, pg.R33]])

T1 = np.array([pg.t1, pg.t2, pg.t3])*1e-3

w1 = np.array( [3376, 2704] )
W1 = w * 1.69e-6

cam1 = Camera(ecran, K1, R1, T1, W1, w1, sgmf1, mask1)
cam1.centre_x=1768; cam1.centre_y=1283; cam1.rayon=6000

# Allied vision -------------------------------------
sgmf2 = "jc_menage/cam_match_AV.png"
mask2 = "jc_menage/conf_AV.png"

K2 =  np.transpose(np.array([[av.K11 , av.K12, av.K13],
             [av.K21, av.K22, av.K23],
             [av.K31,av.K32,av.K33]]))
R2 = np.array([[av.R11 , av.R12, av.R13],
             [av.R21, av.R22, av.R23],
             [av.R31, av.R32, av.R33]])
T2 = np.array([av.t1,av.t2,av.t3])*1e-3

w2 = np.array( [780, 580] )
W2 = w * 8.3e-6

cam2 = Camera(ecran, K2, R2, T2, W2, w2, sgmf2, mask2)
cam2.centre_x=308; cam2.centre_y=235; cam2.rayon=1000

#################################################################
