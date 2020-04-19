import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2
import scipy.signal as sci
from scipy.optimize import curve_fit
plt.close('all')
from Camera import Camera
from Ecran import Ecran
from nc import *
from util import surface_refEcran, montage_refEcran, allo_refEcran,  show_sgmf

# choisir l'échantillon à caractériser parmi la panoplie collector best of 2018-2020 "ah les années poly, c'était beau" :
#lentille_anto, miroir_plan_anto, lentille_biconvexe, lentille_plano_convexe, miroir_plan
echantillon = "lentille_biconvexe"
# NOUS -------------------------------------
import dataPG as pg
import dataAV as av
c = (888,576)
K1 = np.genfromtxt('./calibration/data_PG/camera.txt')
K2 = np.genfromtxt('./calibration/data_AV/camera.txt')
# TONY -------------------------------------
# import dataPG_ as pg  #anthony _
# import dataAV_ as av
# K1=np.transpose(np.array(pg.K)) #anthony
# K2=np.transpose(np.array(av.K))  #anthony
# c=(962, 567) #antho
# -------------------------------------



#################################################################
# Écran -------------------------------------
w = np.array( [1600, 900] ) #pixels
W = w * 0.277e-3 #m
ecran = Ecran( W, w ,c )
# Camera Point Grey -------------------------------------
sgmf1 = "./data/" + echantillon + "/cam_match_PG.png"


R1 = np.array(pg.R)
T1 = np.array(pg.T)
w1 = np.array( [3376, 2704] )
W1 = w * 1.69e-6
cam1 = Camera(ecran, K1, R1, T1, W1, sgmf1)
cam1.mask = np.transpose(cv2.imread("./data/" + echantillon + "/quadrupleconf_PG.png", 0).astype('bool')) #quadrupleconf est meilleure que conf pour PG mais pas pour AV
# Allied vision -------------------------------------
sgmf2 = "./data/" + echantillon + "/cam_match_AV.png"
R2 = np.array(av.R)
T2 = np.array(av.T)
w2 = np.array( [780, 580] )
W2 = w * 8.3e-6
cam2 = Camera(ecran, K2, R2, T2, W2, sgmf2)
cam2.mask = np.transpose(cv2.imread("./data/" + echantillon + '/conf_AV.png', 0).astype('bool'))



#
# ## Comparaison pixels AV et PG rescale sgmf
# plt.plot(np.arange(1,cam1.w[1]+1),cv2.imread(sgmf1)[:,cam1.w[1],1],'o')
# plt.plot(np.arange(1,cam2.w[1]+1)*(cam1.w[1]+1)/(cam2.w[1]+1),(cv2.imread(sgmf2)[:,cam2.w[1],1])*0.8 + 28,'o')
# plt.legend(['PG','AV'])
# plt.xlim([400,470])
# plt.ylim([150,180])


## Comparaison avant et apres filtrage gaussien sur une tranche de sgmf

sgmf = cv2.imread(sgmf1).astype('float64')

tranche_x = 708
plage_x = np.arange(1,int(w1[1]/2)-2)

fig, ax = plt.subplots()
plt.plot(plage_x,sgmf[plage_x,tranche_x,2],'o',markersize=3)
plt.legend(['SGMF brute','Filtrage Median'])


plt.show()


fig, ax = plt.subplots()
im = plt.imshow(sgmf[:,:,2])
ax.xaxis.tick_top()
ax.set_xlabel('u')
ax.xaxis.set_label_position('top')
ax.set_ylabel('v')
cbar = plt.colorbar(im)
plt.axvline(tranche_x,color='r')
plt.show()




#
##################################################################
## # Notre miroir :
## y1=-0.0195; y2=-0.05
#y1=0.1; y2=-0.1
## x1=0.05; x2=-0.04
#x1=0.1; x2=-0.1
#
##direction de recherche normale a lecran
#d = np.array([0,0,1]) #- anthony
#t = np.array([(x1+x2)/2, (y1+y2)/2, 15e-2]) #- anthony
## t = np.array([0.0,0.0, -10e-2])
##direction de recherche normale a une camera
## d = cam1.camToEcran(np.array([0,0,1,0]))[:3]
## t = cam1.camToEcran(np.array([0,0,0,1]))[:3] + d*10e-2
#
#h=0.1e-2
#l=20e-2
#
#grid = []
#o = t
#dk=0.005
#Lx=(x1-x2)/2;
#Ly=(y1-y2)/2;
#kx=int(np.floor(Lx/dk)); ky=int(np.floor(Ly/dk))
#
#
#searchVolumeBasis = graham( d, [1,0,0], [0,1,0] )
#v1 = searchVolumeBasis[0]; v2 = searchVolumeBasis[1]; v3 = searchVolumeBasis[2]
#for j in np.arange(-kx, kx):
#    for i in np.arange(-ky, ky):
#        a = o + i*dk*v3 + j*dk*v2
#        grid.append(a)
#surf=Surface(grid)
#search(surf, d, h, l, cam1, cam2, ecran)
#
## TRAITEMENT DES DONNÉES ------------------------------------------------
#surf.get_good_points(1)
#surf.enr_points_finaux(surf.good_points)
#g = surf.good_points
#
#
##Montrer tout le montage
#L=10e-2 #longueur des flêches
#montage_refEcran(surf, ecran, cam1, cam2, L, t, d)
#surface_refEcran(surf, ecran, cam1, cam2, L, t, d)
## allo_refEcran(g[10], ecran, cam1, cam2, L, t, d)
#
#
## xs,ys,zs = [],[],[]
## for p in g[:]:
##     x=p.vecP[:,0];y=p.vecP[:,1];z=p.vecP[:,2]; noisy_data=p.vecV
##     x=x[noisy_data<0.1];y=y[noisy_data<0.1];z=z[noisy_data<0.1];
##     noisy_data=noisy_data[noisy_data<0.1]
##     if len(noisy_data) > 4:
##         signal = sci.savgol_filter(noisy_data, int(len(noisy_data)/2)*2 - 1 , 2)
##         index = sci.argrelextrema( signal, np.less )[0]
##         if len(index) > 0 :
##             argmin = index[np.argmin( signal[index] )]
##             pmin = z[argmin]; valmin=signal[argmin]
##             xs.append(x[argmin]); ys.append(y[argmin]); zs.append(z[argmin])
##             # plt.figure()
##             # plt.ylabel('||$n_1 x n_2$||')
##             # plt.xlabel('Distance (m)')
##             # plt.plot(-z, noisy_data, label="données", marker='.')
##             # plt.plot(-z, signal, label="lissage")
##             # plt.plot(-pmin, valmin, 'o', label='minimum')
##             # plt.legend(loc=0)
##             # plt.savefig('cac.png', format='png')
##             # plt.show()
##             # show_sgmf(cam1, cam2, p, None)
##
##
##
##
##
## import plotly.graph_objects as go
## import plotly.figure_factory as ff
##
## data  = [go.Mesh3d(
##     x = xs,
##     y = ys,
##     z = zs,
##     # mode = 'markers',
##     # marker = dict(size=9)
##     opacity=0.4
##     )]
##
## data += [go.Mesh3d(
##     x = surf.x_i,
##     y = surf.y_i,
##     z = surf.z_i,
##     # mode = 'markers',
##     # marker = dict(size=9)
##     opacity=0.1
##     )]
##
## fig = go.Figure(data)
##
## fig.update_layout(
## scene = dict(xaxis_title='X', yaxis_title='Y',zaxis_title='Z',     aspectratio=dict(x=1, y=1, z=1),
## aspectmode='manual',
## camera = dict(
## up=dict(x=0, y=0, z=-1),
## center=dict(x=0, y=0, z=0),
## eye=dict(x=1.25, y=1.25, z=-1.25)
## )))
##
##
## fig.update_layout(showlegend=True)
## # fig.write_image("fig_{}.eps".format(stra))
## fig.show()
