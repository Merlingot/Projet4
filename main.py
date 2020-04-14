import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2
import scipy.signal as sci
from scipy.optimize import curve_fit

from Camera import Camera
from Ecran import Ecran
from nc import *
from util import surface_refEcran, montage_refEcran, allo_refEcran,  show_sgmf
import dataPG_ as pg  #anthony _
import dataAV_ as av

plt.close('all')

# Écran
# c = (888,576)
c=(962, 567)
w = np.array( [1600, 900] ) #pixels
W = w * 0.277e-3 #m
ecran = Ecran( W, w ,c )

###################

# choisir l'échantillon à caractériser parmi la panoplie collector best of 2018-2020 "ah les années poly, c'était beau" :
#lentille_anto, miroir_plan_anto, lentille_biconvexe, lentille_plano_convexe, miroir_plan
echantillon = "miroir_plan_anto"


# Camera Point Grey -------------------------------------
sgmf1 = "./data/" + echantillon + "/cam_match_PG.png"
# K1 = np.genfromtxt('./calibration/data_PG/camera.txt')
K1=np.transpose(np.array(pg.K)) #anthony
R1 = np.array(pg.R)
T1 = np.array(pg.T)
w1 = np.array( [3376, 2704] )
W1 = w * 1.69e-6
cam1 = Camera(ecran, K1, R1, T1, W1, sgmf1)
cam1.mask = cv2.imread("./data/" + echantillon + "/conf_PG.png", 0).astype('bool')

# Allied vision -------------------------------------
sgmf2 = "./data/" + echantillon + "/cam_match_AV.png"
# K2 = np.genfromtxt('./calibration/data_AV/camera.txt')
K2=np.transpose(np.array(av.K))  #anthony
R2 = np.array(av.R)
T2 = np.array(av.T)
w2 = np.array( [780, 580] )
W2 = w * 8.3e-6
cam2 = Camera(ecran, K2, R2, T2, W2, sgmf2)
cam2.mask = cv2.imread("./data/" + echantillon + '/conf_AV.png', 0).astype('bool')

#################################################################
# f = cv2.imread('/Users/mariannelado-roy/projet4/TheoUnwraping/fringes/fringes_000.png')
# cam2.sgmf.shape
# plt.colorbar()




 #direction de recherche normale a lecran
d = np.array([0,0,-1]) #- anthony
t = np.array([0.075,0, 0e-2]) #- anthony
# t = np.array([0.0,0.0, -10e-2])
#direction de recherche normale a une camera
# d = cam1.camToEcran(np.array([0,0,1,0]))[:3]
# t = cam1.camToEcran(np.array([0,0,0,1]))[:3]

h=5e-2
l=50e-2

searchVolumeBasis = graham( d, [1,0,0], [0,1,0] )
v1 = searchVolumeBasis[0]; v2 = searchVolumeBasis[1]; v3 = searchVolumeBasis[2]

grid = []
o = t
dk=0.5e-2
Lx=ecran.W[0]/3;
Ly=ecran.W[1]/3;
kx=int(np.floor(Lx/dk)); ky=int(np.floor(Ly/dk))

for j in np.arange(-kx, kx):
    for i in np.arange(-ky, ky):
        a = o + i*dk*v3 + j*dk*v2
        grid.append(a)

surf=Surface(grid)
search(surf, d, h, l, cam1, cam2, ecran)

# TRAITEMENT DES DONNÉES ------------------------------------------------
surf.get_good_points(1)
surf.enr_points_finaux(surf.good_points)
g = surf.good_points


#Montrer tout le montage
L=10e-2 #longueur des flêches
montage_refEcran(surf, ecran, cam1, cam2, L, t, d)


# Descente des normales
allo_refEcran(g[5], ecran, cam1, cam2, L, t, d)

# xs,ys,zs = [],[],[]
# for p in g:
#     x=p.vecP[:,0];y=p.vecP[:,1];z=p.vecP[:,2]; noisy_data=p.vecV
#     # x=x[noisy_data<0.1];y=y[noisy_data<0.1];z=z[noisy_data<0.1];
#     # noisy_data=noisy_data[noisy_data<0.1]
#     # if len(noisy_data) > 1:
#         # print('cul')
#         # signal = sci.savgol_filter(noisy_data, int(len(noisy_data)/2)*2 - 1 , 2)
#         # index = sci.argrelextrema( signal, np.less )[0]
#         # if len(index) > 0 :
#     plt.figure()
#     plt.plot(z, noisy_data, label="noisy data", marker='o')
#     # plt.plot(z, signal, label="filter")
#     # argmin = index[np.argmin( signal[index] )]
#     # pmin = z[argmin]; valmin=signal[argmin]
#     # xs.append(x[argmin]); ys.append(y[argmin]); zs.append(z[argmin])
#     # plt.plot(pmin, valmin, 'o')
#     # plt.legend(loc=0)
#     plt.show()
#
#     show_sgmf(cam1, cam2, p, None)
#
