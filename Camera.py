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

        self.S = self.camToEcran( np.array([0,0,0]) )

        self.centre_x=None
        self.centre_y=None
        self.rayon=None

        ## SGMF
        #-Importing cartography
        sgmfXY = cv2.imread(sgmf)
        sgmfXY = sgmfXY.astype('float64')

        #-Green channel
        self.sgmf = np.zeros( (sgmfXY.shape[0], sgmfXY.shape[1], sgmfXY.shape[2]-1) )
        self.sgmf[:,:,0] = sgmfXY[:,:,1] * self.ecran.w[0] / 255.
        self.sgmf[:,:,1] = sgmfXY[:,:,2] * self.ecran.w[1] / 255.


    def ecranToCam(self, Pe):
        """ Ref ecran -> cam"""
        return self.R@Pe + self.T

<<<<<<< HEAD

=======
    def camToEcran(self, Pc):
        """ Ref cam -> l'écran"""
        return np.linalg.inv(self.R)@(Pc - self.T)

    def camToCCD(self, C):
        """ [x,y,z]-> [x,y,z] """
        return -self.F/C[2]*C
>>>>>>> marinouille

    def spaceToPixel(self, vecSpace):
        """
        Args:
        vecSpace: np.array([x,y])
            Vecteur de position en m
        Returns:
            np.array([u,v])
            Vecteur de position en pixel
        """
        vec = np.array([ vecSpace[0], vecSpace[1], self.F])

        vecPix = self.K@vec
        vx, vy = vecPix[0], vecPix[1]

        if vx > 1 and vy > 1 and vx < self.sgmf.shape[0]-1 and vy < self.sgmf.shape[1]-1:
            if ( (vx-self.centre_x)**2 + (vy-self.centre_y)**2 < self.rayon**2 ):
                self.U.append(np.array([vx,vy]))
            return np.array([vx,vy])
        else:
            # return np.array([0,0])
            return None

    def pixCamToEcran(self, u):

<<<<<<< HEAD
        uE = [int(np.floor(u[0])), int(np.floor(u[1]))]
        uR = np.mod(u,1)

        if uE[0] > 1 and uE[1] > 1 and uE[0] < self.sgmf.shape[0]-1 and uE[1] < self.sgmf.shape[1]-1:

            vx = self.sgmf[uE[0],uE[1],0] + uR[0]*( self.sgmf[uE[0]+1, uE[1]+1, 0] - self.sgmf[uE[0],uE[1],0] )
            vy = self.sgmf[uE[0],uE[1],1] + uR[1]*( self.sgmf[uE[0]+1, uE[1]+1, 1] - self.sgmf[uE[0],uE[1],1] )
=======
        """ ATTENTION : A reverifier floor pour valeurs négatives """
>>>>>>> marinouille

        uE = [int(np.floor(u[0])), int(np.floor(u[1]))] #entier
        uR = np.mod(u,1) #reste

        # if uE[0] > 1 and uE[1] > 1 and uE[0] < self.sgmf.shape[0]-1 and uE[1] < self.sgmf.shape[1]-1:

        vx = self.sgmf[uE[0],uE[1],0] + uR[0]*( self.sgmf[uE[0]+1, uE[1]+1, 0] - self.sgmf[uE[0],uE[1],0] )
        vy = self.sgmf[uE[0],uE[1],1] + uR[1]*( self.sgmf[uE[0]+1, uE[1]+1, 1] - self.sgmf[uE[0],uE[1],1] )

        return np.array([vx, vy])
