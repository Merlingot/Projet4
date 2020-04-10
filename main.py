import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2
from skimage.io import imread, imsave
import seaborn as sns
import scipy.signal as sci

from Camera import Camera
from Ecran import Ecran
from nc import *
from util import *
import dataPG as pg
import dataAV as av

plt.close('all')

# Écran
c = (962,567)
w = np.array( [1600, 900] ) #pixels
W = w * 0.277e-3 #m
ecran = Ecran( W, w ,c )

###################
# Camera Point Grey -------------------------------------
sgmf1 = "./13mars/lentille_biconvexe/cam_match_PG.png"

K1 = np.genfromtxt('./calibration/data_PG/camera.txt')
# K1=np.transpose(np.array(pg.K))
R1 = np.array(pg.R)
T1 = np.array(pg.T)

w1 = np.array( [3376, 2704] )
W1 = w * 1.69e-6

cam1 = Camera(ecran, K1, R1, T1, W1, w1, sgmf1)

# Allied vision -------------------------------------
sgmf2 = "./13mars/lentille_biconvexe/cam_match_AV.png"

K2 = np.genfromtxt('./calibration/data_AV/camera.txt')
# K2=np.transpose(np.array(av.K))
R2 = np.array(av.R)
T2 = np.array(av.T)

w2 = np.array( [780, 580] )
W2 = w * 8.3e-6

cam2 = Camera(ecran, K2, R2, T2, W2, w2, sgmf2)

#################################################################

d = np.array([0,0,1])
t = np.array([0,0,0])

h=0.1e-2
l=60e-2

searchVolumeBasis = graham( d, [1,0,0], [0,1,0] )

v1 = searchVolumeBasis[0]
v2 = searchVolumeBasis[1]
v3 = searchVolumeBasis[2]

grid = []
o = t
dk=1e-2
Lx=ecran.W[0]
Ly=ecran.W[1]
kx=int(np.floor(Lx/dk))
ky=int(np.floor(Ly/dk))

for j in np.arange(-kx, kx):
    for i in np.arange(-ky, ky):
        a = o + i*dk*v3 + j*dk*v2
        grid.append(a)

surf=Surface(grid)
a=len(grid)
search(surf, d, h, l, cam1, cam2, ecran)
surf.get_good_points(0.1)

final_points=[]
for p in surf.good_points:
    if len(p.vecV) > 4:
        s=int(len(p.vecV)/4)*2 + 1
        signal = sci.savgol_filter(p.vecV,s, 2)
        index = sci.argrelextrema(signal, np.less)[0]
        if len(index)==1:
            final_points.append(p)
            p.pfinal=p.vecP[index[0]]
            p.vfinal= p.vecV[index[0]]
            plt.figure()
            fig, ax2 = plt.subplots(1,1)
            ax2.plot(p.vecP[:,2], p.vecV, '.')
            ax2.plot(p.pmin[2], p.valmin, 'rx')
            ax2.plot(p.pfinal[2], p.vfinal, 'bo')
            ax2.plot(p.vecP[:,2], signal)
            plt.show()

b=len(final_points)
surf.enr_points_finaux(final_points)
#Visualisation
L=5e-2 #longueur des flêches
montage_refEcran(surf, ecran, cam1, cam2, L, t, d)
grilles_refEcran(surf, ecran, cam1, cam2, L, t, d)
print(b/a*100)


#
