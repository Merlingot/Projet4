import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2
from skimage.io import imread, imsave
import seaborn as sns
import scipy.signal as sci
from scipy.optimize import curve_fit

from Camera import Camera
from Ecran import Ecran
from nc import *
from util import surface_refEcran, montage_refEcran, allo_refEcran,  show_sgmf
import dataPG_ as pg
import dataAV_ as av

plt.close('all')

# Écran
c = (888,576)
w = np.array( [1600, 900] ) #pixels
W = w * 0.277e-3 #m
ecran = Ecran( W, w ,c )

###################
# Camera Point Grey -------------------------------------
sgmf1 = "./data/lentille_anto/cam_match_PG.png"
# K1 = np.genfromtxt('./calibration/data_PG/camera.txt')
K1=np.transpose(np.array(pg.K))
R1 = np.array(pg.R)
T1 = np.array(pg.T)

w1 = np.array( [3376, 2704] )
W1 = w * 1.69e-6
cam1 = Camera(ecran, K1, R1, T1, W1, sgmf1)
cam1.mask = cv2.imread('./data/lentille_anto/conf_PG.png', 0).astype('bool')

# Allied vision -------------------------------------
sgmf2 = "./data/lentille_anto/cam_match_AV.png"

# K2 = np.genfromtxt('./calibration/data_AV/camera.txt')
K2=np.transpose(np.array(av.K))
R2 = np.array(av.R)
T2 = np.array(av.T)

w2 = np.array( [780, 580] )
W2 = w * 8.3e-6

cam2 = Camera(ecran, K2, R2, T2, W2, sgmf2)
cam2.mask = cv2.imread('./data/lentille_anto/allo.png', 0).astype('bool')
#################################################################



d = np.array([0,0,-1])
t = np.array([0,0,-20e-2])

h=0.05e-2
l=20e-2

searchVolumeBasis = graham( d, [1,0,0], [0,1,0] )
v1 = searchVolumeBasis[0]; v2 = searchVolumeBasis[1]; v3 = searchVolumeBasis[2]

grid = []
o = t
dk=0.5e-2
Lx=ecran.W[0]/4;
Ly=ecran.W[1]/4
kx=int(np.floor(Lx/dk)); ky=int(np.floor(Ly/dk))

for j in np.arange(-kx, kx):
    for i in np.arange(-ky, 0):
        a = o + i*dk*v3 + j*dk*v2
        grid.append(a)

# grid = [np.array( [0.03 , -0.06 , -0.25])]


surf=Surface(grid)
search(surf, d, h, l, cam1, cam2, ecran)


# # TRAITEMENT DES DONNÉES ------------------------------------------------
surf.get_good_points(0.1)
# # Visualisation
surf.enr_points_finaux(surf.good_points)

L=10e-2 #longueur des flêches
montage_refEcran(surf, ecran, cam1, cam2, L, t, d)
# surface_refEcran(surf, ecran, cam1, cam2, L, t, d)
g = surf.good_points
show_sgmf(cam1, cam2, g[0], 0.1)

allo_refEcran(g[0], ecran, cam1, cam2, L, t, d)
