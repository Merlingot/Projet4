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
c =  (888,576)
# c = (962,567)
w = np.array( [1600, 900] ) #pixels
W = w * 0.277e-3 #m
ecran = Ecran( W, w ,c )

###################
# Camera Point Grey -------------------------------------
sgmf1 = "jc_menage/cam_match_PTG.png"
mask1 = "jc_menage/conf_PG.png"

K1 = np.array([[5849.19542915438, 0.0, 892.9111951860172],
[ 0.0, 5836.7115487610945, 456.9121564783766],
[0.0, 0.0, 1.0] ])

R1 =  np.array( [ [0.03072236566588105, 0.9945582807691511, 0.09954879407306896],
 [-0.7421423568919123, -0.04401693036176985, 0.6687953587970273],
 [0.6695377945678715, -0.09442635222774159, 0.7367515223263222]])

T1 = np.array([-0.02210242299820603,
 -0.1325854601537139,
 0.2467493804368752])

w1 = np.array( [3376, 2704] )
W1 = w * 1.69e-6

cam1 = Camera(ecran, K1, R1, T1, W1, w1, sgmf1, mask1)
cam1.centre_x=1768; cam1.centre_y=1283; cam1.rayon=6000

# Allied vision -------------------------------------
sgmf2 = "jc_menage/cam_match_AV.png"
mask2 = "jc_menage/conf_AV.png"

K2 =  np.array([[1944.8733876716499 , 0, 408.6971225310835],
             [0, 1941.2047651701032 , 310.66335685827215],
             [0,0,1]])

R2 = np.array([[-0.08412538109416318, 0.9960717278018529, -0.02764115282677471],
 [-0.8002799530673839, -0.05100994976114542, 0.5974529117376792],
 [0.5936959802577643, 0.07238161437268931, 0.8014274670402654]])

T2  = np.array([-0.01279800501154558, -0.1449574519762213, 0.1519862825587646])

w2 = np.array( [780, 580] )
W2 = w * 8.3e-6

cam2 = Camera(ecran, K2, R2, T2, W2, w2, sgmf2, mask2)
cam2.centre_x=308; cam2.centre_y=235; cam2.rayon=1000

#################################################################

d = np.array([0,0,-1])
t = np.array([0,0,0])

h=10e-2
precision=1e-2
l=0e-2

searchVolumeBasis = graham( d, [1,0,0], [0,1,0] )

v1 = searchVolumeBasis[0]
v2 = searchVolumeBasis[1]
v3 = searchVolumeBasis[2]

grid = []
o = t + np.array([0.10, 0, -0.10])
dk=1e-2
Lx=ecran.W[0]/3
Ly=ecran.W[1]/2
kx=int(np.floor(Lx/dk))
ky=int(np.floor(Ly/dk))

for j in np.arange(-kx, kx):
    for i in np.arange(-ky, ky):
        a = o + i*dk*v3 + j*dk*v2
        grid.append(a)

surf= Surface(grid)
search(surf, d, h, l, precision, cam1, cam2, ecran)

#Visualisation
L=10e-2 #longueur des flêches
montage_refEcran(surf, ecran, cam1, cam2, L, t, d)
