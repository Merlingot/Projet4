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

K1 = np.array([[10346.82, 0., 0.],
             [0., 10347.03, 0.],
             [1611.22, 1363.49, 1.]])

R1 = np.array([[-0.998, 0.01193, 0.01183],
             [-0.003297, 0.7564, -0.6541],
             [-0.02205, -0.6540, -0.7262]])

T1 = np.array([56.368, -156.815, 142.289])*1e-3


w1 = np.array( [3376, 2704] )
W1 = w * 1.69e-6

sgmf1 = "cam_match_PTG.png"

cam1 = Camera(ecran, K1, R1, T1, W1, w1, sgmf1)

####################
# Camera Allied Vision

K2 = np.array([[1996.64, 0., 0.],
             [0., 1997.1, 0.],
             [385.25, 286.69, 1.]])

R2 = np.array([[-0.9966, -0.05773, -0.05948],
             [-0.006757, 0.7718, -0.6358],
             [0.08262, -0.6333, -0.7659]])

T2 = np.array([13.535, -156.640, 124.790])*1e-3

w2 = np.array( [780, 580] )
W2 = w * 8.3e-6

sgmf2 = "cam_match_AV.png"

cam2 = Camera(ecran, K2, R2, T2, W2, w2, sgmf2)

### Reconstruction
#x=np.linspace(-100,50, num=20)*1e-2
#y=np.linspace(-100, 50, num=20)*1e-2

#Z=20e-2

#for i in range(len(x)):
#    for j in range(len(y)):
#        grid.append( np.array( [x[i], y[j], Z] ) )


d=getApproxZDirection(cam1.R, cam2.R) #référentiel de l'écran
h=1e-3
precision=1e-2

searchVolumeBasis = graham( d, [0,0,1], [0,1,0] )

v1 = searchVolumeBasis[0]
v2 = searchVolumeBasis[1]
v3 = searchVolumeBasis[2]

grid = []
o = [0,0,0]
dk = 1e-3
k = 15
for i in np.arange(-k, k):
    for j in np.arange(-k, k):
        a = o + i*dk*v2 + j*dk*v3
        grid.append(a)

surf = search(d, h, grid, precision, cam1, cam2, ecran)

fig=plt.figure()
ax=fig.add_subplot(111, projection='3d')

for i in surf.points:
    ax.scatter( i.xyz[0], i.xyz[1], i.xyz[2])

dirCam1 = np.dot(cam1.R, np.array([0,0,-1])) * 20
dirCam2 = np.dot(cam2.R, np.array([0,0,-1])) * 20
ax.scatter(0,0,0)
ax.scatter(cam1.S[0], cam1.S[1], cam1.S[2])
ax.scatter(cam2.S[0], cam2.S[1], cam2.S[2])
ax.quiver(0,0,0,0,0,20)
ax.quiver(cam1.S[0], cam1.S[1], cam1.S[2], dirCam1[0], dirCam1[1], dirCam1[2])
ax.quiver(cam2.S[0], cam2.S[1], cam2.S[2], dirCam2[0], dirCam2[1], dirCam2[2])

plt.show()
