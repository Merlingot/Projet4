import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage.io import imread, imsave
import seaborn as sns


class Camera:

    """
    Input:
        -K      : Matrice intrinsèque de la camera contenant (fx,fy,s,cx,cy)             | np.narray()
        -R      : Matrice de rotation pour le passage entre ref_{ecran} -> ref_{cam}     | np.narray()
        -T      : Matrice de translation pour le passage entre ref_{ecran} -> ref{cam}   | np.narray()
        -W      : Vecteur de la taille du CCD de la camera en [mm]                       | np.array()
        -w      : Vecteur de la taille du CCD de la camera en [pix]                      | np.array()
        -SGMF   : String du nom du PNG de cartographie de pixel entre camera et ecran | str()
    """
    def __init__(self, ecran, K, R, T, W, w, sgmf, mask):

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

        self.M = np.block([ [R , T.reshape(3,1)] ,
                [ np.zeros((1,3)).reshape(1,3) , 1]
                ])

        self.F = ( K[0,0]*self.sx + K[1,1]*self.sy ) / 2. #Focale utile

        self.S = self.camToEcran( np.array([0,0,0]) )

        self.centre_x=None
        self.centre_y=None
        self.rayon=None

        ## SGMF
        #-Importing cartography
        sgmfXY = cv2.imread(sgmf)
        sgmfXY = sgmfXY.astype('float64')

        #-Importing confidence mask
        self.mask = cv2.imread(mask).astype('int')

        #-Green channel
        self.sgmf = np.zeros( (sgmfXY.shape[0], sgmfXY.shape[1], sgmfXY.shape[2]-1) )
        self.sgmf[:,:,0] = sgmfXY[:,:,1] * self.ecran.w[0] / 255.
        self.sgmf[:,:,1] = sgmfXY[:,:,2] * self.ecran.w[1] / 255.


    def ecranToCam(self, P):
        """
        * homogene
        [px, py, pz, 1] -> [px', py', pz', 1] """
        return self.M@P

    def camToEcran(self, P):
        """ [px', py', pz'] -> [px, py, pz]"""
        Rinv = np.linalg.inv(self.R)
        return Rinv@(P-self.T)

    def camToCCD(self, C):
        """
        * homogene
        [px', py', pz', 1] -> [U,V,F,1] """
        pzp=C[2]
        loic = np.block( [ [ np.eye(3) , np.zeros((3,1)).reshape(3,1) ],
                [np.zeros((1,3)).reshape(1,3) , pzp/self.F]
                ])
        return -self.F/pzp*loic@C

    def spaceToPixel(self, vecSpace):
        """
        * homogene
        Args:
        vecSpace: np.array([U,V,F,1])
            Vecteur de position en m
        Returns:
            np.array([u,v,1])
            Vecteur de position en pixel
        """
        loic = np.block( [ self.K , np.zeros((3,1))] )
        vecPix = (1/self.F)*loic@vecSpace
        u, v = vecPix[0], vecPix[1]

        if u > 1 and v > 1 and u < self.sgmf.shape[0]-1 and v < self.sgmf.shape[1]-1:
            if ( (u-self.centre_x)**2 + (v-self.centre_y)**2 < self.rayon**2 ):
                if np.abs( v - self.centre_y ) < np.sqrt(2)/2*self.rayon:
                    self.U.append(np.array([u,v]))
                    return np.array([u,v,1])
            else:
                # return np.array([0,0])
                return None
        else:
            return None

    def pixCamToEcran(self, vecPix):

        """
        * homogene
        [u,v,1] -> [u',v',1]
        """

        uE = [int(np.floor(vecPix[0])), int(np.floor(vecPix[1]))] #entier
        uR = np.mod(vecPix,1) #reste

        up = self.sgmf[uE[0],uE[1],0] + uR[0]*( self.sgmf[uE[0]+1, uE[1]+1, 0] - self.sgmf[uE[0],uE[1],0] )
        vp = self.sgmf[uE[0],uE[1],1] + uR[1]*( self.sgmf[uE[0]+1, uE[1]+1, 1] - self.sgmf[uE[0],uE[1],1] )

        return np.array([up, vp, 1])
