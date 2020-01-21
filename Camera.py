import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage.io import imread, imsave
import seaborn as sns

class Camera:

    """
    Input:
       -K : Matrice intrinsèque de la camera contenant (fx,fy,s,cx,cy)             | np.narray()
       -R : Matrice de rotation pour le passage entre ref_{ecran} -> ref_{cam}     | np.narray()
      -T : Matrice de translation pour le passage entre ref_{ecran} -> ref{cam}   | np.narray()
       -W : Vecteur de la taille du CCD de la camera en [mm]                       | np.array()
       -w : Vecteur de la taille du CCD de la camera en [pix]                      | np.array()
       -SGMF : String du nom du PNG de cartographie de pixel entre camera et ecran | str()
    """
    def __init__(self, ecran, K, R, T, W, w, sgmf):

        # Setup
        self.ecran = ecran

        self.U = []

        # Intrinsèque
        self.K = K                              # Tout information
        self.f = ( K[0,0] + K[1,1] ) / 2.       # Focale camera (moyenne de fx et fy)
        self.c = np.array( [K[2,0], K[2,1]] )   # Centre optique du CCD [pix, pix]
        self.s = K[1,0]                         # Skew
        self.W = W                              # Taille du CCD en [m]
        self.w = w                              # Taille du CCD en [pix]

        self.sx = W[0]/w[0]                     #[m/pixels]
        self.sy = W[1]/w[1]

        # Extrinsèque (Ecran -> Camera)
        self.R = R                              # Matrice de rotation
        self.T = T                              # Matrice de translation

        self.F = ( K[0,0]*self.sx + K[1,1]*self.sy ) / 2. #Focale utile

        self.S = np.linalg.inv(self.R)@self.T


        ## SGMF
        #-Importing cartography
        sgmfXY = cv2.imread(sgmf)
        sgmfXY = sgmfXY.astype('float64')

        #-Green channel
        self.sgmf = np.zeros( (sgmfXY.shape[0], sgmfXY.shape[1], sgmfXY.shape[2]-1) )
        self.sgmf[:,:,0] = sgmfXY[:,:,1] * self.ecran.w[0] / 255.
        self.sgmf[:,:,1] = sgmfXY[:,:,2] * self.ecran.w[1] / 255.



    def spaceToPixel(self, vecSpace):
        """
        ATTENTION
        Args:
        vecSpace: np.array([x,y])
            Vecteur de position en m
        Returns:
            np.array([u,v])
            Vecteur de position en pixel
        """
        x, y = vecSpace[0], vecSpace[1]

        vx, vy = (x/self.sx + self.c[0]), (y/self.sy-self.c[1]) ##-1 pourquoi??

        if vx > 1 and vy > 1 and vx < self.sgmf.shape[0]-1 and vy < self.sgmf.shape[1]-1:
            self.U.append(np.array([vx,vy]))
            return np.array([vx,vy])
        else:
            self.U.append(np.array([0,0]))
            return np.array([0,0])

    def pixCamToEcran(self, u):

        uE = [int(np.floor(u[0])), int(np.floor(u[1]))] #entier
        uR = np.mod(u,1) #reste

        if uE[0] > 1 and uE[1] > 1 and uE[0] < self.sgmf.shape[0]-1 and uE[1] < self.sgmf.shape[1]-1:

            vx = self.sgmf[uE[0],uE[1],0] + uR[0]*( self.sgmf[uE[0]+1, uE[1]+1, 0] - self.sgmf[uE[0],uE[1],0] )
            vy = self.sgmf[uE[0],uE[1],1] + uR[1]*( self.sgmf[uE[0]+1, uE[1]+1, 1] - self.sgmf[uE[0],uE[1],1] )

            return np.array([vx, vy])

        else:  #Confidence map ?
            return np.array([0,0,0])
            # return None
