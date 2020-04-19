import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import cv2
import scipy.signal as sci
from scipy.optimize import curve_fit
from scipy.interpolate import UnivariateSpline, SmoothBivariateSpline, RectBivariateSpline
plt.close('all')
from Camera import Camera
from Ecran import Ecran






#################################################################


#ne fonctionne pas avec .._anto, (trop grosses dimensions pour la univariate smoothing)

# choisir l'échantillon à caractériser parmi la panoplie collector best of 2018-2020 "ah les années poly, c'était beau" :
#miroir_plan_anto, lentille_biconvexe, lentille_plano_convexe, miroir_plan
echantillon = "lentille_plano_convexe"






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




#################################################################

###### Caméra POINT GREY

#là je suis perdu avec les 0 ou end-1 ... je sais pas si quand je montre shape ça me dit le dernier indice ou le nombre de cases. donc j'efface pas 

plage_x= np.arange(0,int(w1[1]/2)-1)
plage_y= np.arange(0,int(w1[0]/2)-1)


sgmf = cv2.imread(sgmf1)
sgmf_median = cv2.medianBlur(sgmf,5)
data_v = sgmf_median[:,:,1]
data_u = sgmf_median[:,:,2]



FULL_SGMF = np.zeros([len(plage_x),len(plage_y),2])

for tranche_x in plage_y :
    sgmf_continuous_1D = UnivariateSpline(plage_x, data_v[plage_x,tranche_x])
    FULL_SGMF[plage_x,tranche_x,1] = sgmf_continuous_1D(plage_x)
    
for tranche_y in plage_x :
    sgmf_continuous_1D = UnivariateSpline(plage_y, data_u[tranche_y,plage_y])
    FULL_SGMF[tranche_y,plage_y,0] = sgmf_continuous_1D(plage_y)


np.save("./data/" + echantillon + "/cam_match_PG",FULL_SGMF)





###### Caméra ALLIED VISION

#là je suis perdu avec les 0 ou end-1 ... je sais pas si quand je montre shape ça me dit le dernier indice ou le nombre de cases. donc j'efface pas 

plage_x= np.arange(0,int(w2[1])-1)
plage_y= np.arange(0,int(w2[0])-1)


sgmf = cv2.imread(sgmf1)
sgmf_median = cv2.medianBlur(sgmf,5)
data_v = sgmf_median[:,:,1]
data_u = sgmf_median[:,:,2]



FULL_SGMF = np.zeros([len(plage_x),len(plage_y),2])

for tranche_x in plage_y :
    sgmf_continuous_1D = UnivariateSpline(plage_x, data_v[plage_x,tranche_x])
    FULL_SGMF[plage_x,tranche_x,1] = sgmf_continuous_1D(plage_x)
    
for tranche_y in plage_x :
    sgmf_continuous_1D = UnivariateSpline(plage_y, data_u[tranche_y,plage_y])
    FULL_SGMF[tranche_y,plage_y,0] = sgmf_continuous_1D(plage_y)


np.save("./data/" + echantillon + "/cam_match_AV",FULL_SGMF)