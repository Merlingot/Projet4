import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2
from skimage.io import imread, imsave
import seaborn as sns

from Camera import Camera
from Ecran import Ecran
from nc import *

# Setup
w = np.array( [1600, 900] )
W = w * 0.277e-3
c = np.array( [800, 450] )
ecran = Ecran( W, w, c)

########################################################
## Parametre de calibration provenant de l'annee derniere

###################
# Camera Point Grey

K1 = np.transpose( np.array([[10346.82, 0., 0.],
             [0., 10347.03, 0.],
             [1611.22, 1363.49, 1.]]) )

R1 = np.array([[-0.998, 0.01193, 0.01183],
             [-0.003297, 0.7564, -0.6541],
             [-0.02205, -0.6540, -0.7262]])

T1 = np.array([56.368, -156.815, 142.289])*1e-3


w1 = np.array( [3376, 2704] )
W1 = w * 1.69e-6

sgmf1 = "cam_match_PTG.png"
mask1 = "conf_PG.png"

cam1 = Camera(ecran, K1, R1, T1, W1, w1, sgmf1, mask1)
cam1.centre_x=1942; cam1.centre_y=1493; cam1.rayon=1000

####################
# Camera Allied Vision

K2 = np.transpose( np.array([[1996.64, 0., 0.],
             [0., 1997.1, 0.],
             [385.25, 286.69, 1.]]) )

R2 = np.array([[-0.9966, -0.05773, -0.05948],
             [-0.006757, 0.7718, -0.6358],
             [0.08262, -0.6333, -0.7659]])

T2 = np.array([13.535, -156.640, 124.790])*1e-3

w2 = np.array( [780, 580] )
W2 = w * 8.3e-6

sgmf2 = "cam_match_AV.png"
mask2 = "conf_AV.png"

cam2 = Camera(ecran, K2, R2, T2, W2, w2, sgmf2, mask2)
cam2.centre_x=220; cam2.centre_y=270; cam2.rayon=210


d=getApproxZDirection(cam1, cam2) #référentiel de l'écran
t=(cam1.S+cam2.S)/2

h=1e-3
precision=1e-2
l=60e-2

searchVolumeBasis = graham( d, [0,0,1], [0,1,0] )

# v1 = searchVolumeBasis[0]
# v2 = searchVolumeBasis[1]
# v3 = searchVolumeBasis[2]

v2=(cam2.S-cam1.S)/np.linalg.norm((cam2.S-cam1.S))
v3=(-cam2.S)/np.linalg.norm((cam2.S))

grid = []
o = t
dk = 1e-2
Lx=np.max( [cam1.S[0], cam2.S[0]] )
Ly=np.max( [cam1.S[1], cam2.S[1]] )
kx=int(np.floor(Lx/dk))
ky=int(np.floor(Ly/dk))

for j in np.arange(-kx, kx):
    for i in np.arange(0, 2*ky):
        a = o + i*dk*v3 + j*dk*v2
        grid.append(a)

surf = search(d, h, l, grid, precision, cam1, cam2, ecran)

fig=plt.figure()
ax = Axes3D(fig, azim=-32, elev=1)
ax.auto_scale_xyz([0, 1], [0, 1], [0, 1])

for i in surf.points:
    ax.scatter( i.xyz[0], i.xyz[1], i.xyz[2], marker='.', color='r')

## Set aspect -----------------------------------------
X=np.array([0, cam1.S[0]])
Y=np.array([0, cam1.S[1]])
Z=np.array([0, cam1.S[2]])
# Create cubic bounding box to simulate equal aspect ratio
max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())
# Comment or uncomment following both lines to test the fake bounding box:
for xb, yb, zb in zip(Xb, Yb, Zb):
   ax.plot([xb], [yb], [zb], 'w')
## Set aspect -----------------------------------------


L=1e-2 #Longueur flêches
dirCam1 = cam1.camToEcran(np.array([0,0,1]))*L
dirCam2 = cam2.camToEcran(np.array([0,0,1]))*L
ax.scatter(0,0,0)
ax.scatter(cam1.S[0], cam1.S[1], cam1.S[2], marker='x')
ax.scatter(cam2.S[0], cam2.S[1], cam2.S[2], marker='x')
ax.quiver(0,0,0,0,0,-L)
ax.quiver(t[0],t[1],t[2], d[0]*L, d[1]*L, d[2]*L)
ax.quiver(cam1.S[0], cam1.S[1], cam1.S[2], dirCam1[0], dirCam1[1], dirCam1[2])
ax.quiver(cam2.S[0], cam2.S[1], cam2.S[2], dirCam2[0], dirCam2[1], dirCam2[2])
#ax.set_zlim(np.min(z), np.max(z))

plt.show()
