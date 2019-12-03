import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage.io import imread, imsave
import seaborn as sns

class Camera:

    ############
    # Input:
    #   -K : Matrice intrinsèque de la camera contenant (fx,fy,s,cx,cy)             | np.narray()
    #   -R : Matrice de rotation pour le passage entre ref_{ecran} -> ref_{cam}     | np.narray()
    #   -T : Matrice de translation pour le passage entre ref_{ecran} -> ref{cam}   | np.narray()
    #   -W : Vecteur de la taille du CCD de la camera en [mm]                       | np.array()
    #   -w : Vecteur de la taille du CCD de la camera en [pix]                      | np.array()
    #   -SGMF : String du nom du PNG de cartographie de pixel entre camera et ecran | str()
    ############
    def __init__(self, K, R, T, W, w, sgmf):
        
        # Intrinsèque
        self.K = K                              # Tout information
        self.f = ( K[0,0] + K[1,1] ) / 2.       # Focale camera (moyenne de fx et fy)
        self.c = np.array( [K[2,0], K[2,1]] )   # Centre optique du CCD [pix, pix]
        self.s = K[1,0]                         # Skew
        self.W = W                              # Taille du CCD en [mm]
        self.w = w                              # Taille du CCD en [pix]
        
        # Extrinsèque (Ecran -> Camera)
        self.R = R                              # Matrice de rotation
        self.T = T                              # Matrice de translation

    
        ## SGMF
        #-Importing cartography
        sgmfXY = cv2.imread(sgmf)
        sgmfXY = sgmfXY.astype('float64')

        #-Green channel
        self.sgmf = np.zeros( (sgmfXY.shape[0], sgmfXY.shape[1], sgmfXY.shape[2]-1) )
        self.sgmf[:,:,0] = sgmfXY[:,:,1] * self.w[0] / 255.
        self.sgmf[:,:,1] = sgmfXY[:,:,2] * self.w[1] / 255.

        #-Pixel to Pixel cartography
        plt.figure()
        axy = sns.heatmap(self.sgmf[:,:,0], cmap="coolwarm")

        plt.figure()
        axx = sns.heatmap(self.sgmf[:,:,1], cmap="coolwarm")

        plt.show()





