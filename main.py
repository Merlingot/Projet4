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

sgmf1 = "/home/labo/DATA/9 mars/lentille_03_09_20/cam_match_PG.png"
mask1 = "/home/labo/Projet4/jc_menage/conf_PG.png"

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
sgmf2 = "/home/labo/DATA/9 mars/lentille_03_09_20/cam_match_AV.png"
mask2 = "/home/labo/Projet4/jc_menage/conf_AV.png"

cam2 = Camera(ecran, K2, R2, T2, W2, w2, sgmf2, mask2)
cam2.centre_x=308; cam2.centre_y=235; cam2.rayon=245


#################################################################


#d=getApproxZDirection(cam1, cam2) #référentiel de l'écran
d = np.array([0,0,-1])
#t=(cam1.S+cam2.S)/2
t = np.array([0, 0, 0])

h=50e-2
precision=1e-2
l=10000e-2

searchVolumeBasis = graham( d, [1,0,0], [0,1,0] )

v1 = searchVolumeBasis[0]
v2 = searchVolumeBasis[1]
v3 = searchVolumeBasis[2]
#v3=np.array([0,1,0])
#v2=np.array([1,0,0])

grid = []
o = t
dk=20e-2
Lx=100e-2
Ly=100e-2
kx=int(np.floor(Lx/dk))
ky=int(np.floor(Ly/dk))

for j in np.arange(0, kx):
    for i in np.arange(-ky, 0):
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


L=100e-2 #Longueur flêches
dirCam1 = cam1.camToEcran(np.array([0,0,1]))*L
dirCam2 = cam2.camToEcran(np.array([0,0,1]))*L
ax.scatter(0,0,0)
ax.scatter(cam1.S[0], cam1.S[1], cam1.S[2], marker='x',color='blue')
ax.scatter(cam2.S[0], cam2.S[1], cam2.S[2], marker='x')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
ax.quiver(0,0,0,0,0,-L)
ax.quiver(t[0],t[1],t[2], d[0]*L, d[1]*L, d[2]*L)
ax.quiver(cam1.S[0], cam1.S[1], cam1.S[2], dirCam1[0], dirCam1[1], dirCam1[2])
ax.quiver(cam2.S[0], cam2.S[1], cam2.S[2], dirCam2[0], dirCam2[1], dirCam2[2])
#ax.set_zlim(np.min(z), np.max(z))

plt.show()
