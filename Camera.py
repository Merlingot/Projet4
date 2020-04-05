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
        self.fx=K[0,0]; self.fy=K[1,1]
        self.cu=K[0,2]; self.cv=K[1,2]
        self.K = K                              # Tout information
        self.f = ( self.fx + self.fy ) / 2.       # Focale camera [fx,fy]=pixels (moyenne de fx et fy)
        self.c = np.array([self.cu, self.cv])   # Centre optique du CCD [pix, pix]
        self.s = K[0,1]                         # Skew
        self.W = W                              # Taille du CCD en [W]=m
        self.w = w                              # Taille du CCD en [w]=pixels

        self.sx = W[0]/w[0]                     # Taille d'un pixel [m/pixel]
        self.sy = W[1]/w[1]                     # Taille d'un pixel [m/pixel]

        # Extrinsèque (Ecran -> Camera)
        self.R = R                              # Matrice de rotation [-]
        self.T = T                              # Matrice de translation [m]

        self.eToC = np.block([ [R , T.reshape(3,1)] ,
                [ np.zeros((1,3)).reshape(1,3) , 1]
                ])
        self.cToE = np.block([ [np.transpose(R) , -(np.transpose(R)@T).reshape(3,1)] ,
                [ np.zeros((1,3)).reshape(1,3) , 1]
                ])

        self.F = ( self.fx*self.sx + self.fy*self.sy ) / 2. #Focale utile [m]

        # Position du sténopé de la caméra dans le référentiel de l'écran (même chose que self.T)
        self.S = self.camToEcran( np.array([0,0,0]) )
        self.normale = np.transpose(self.R)@np.array([0,0,1])

        # Pour les masques cheap (À enlever éventuellement)
        self.centre_x=None
        self.centre_y=None
        self.rayon=None

        ## SGMF
        #-Importing cartography
        sgmfXY = cv2.imread(sgmf).astype('float64')

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
        return self.eToC@P

    def camToEcran(self, P):
        """
        * Pas homogene
        [px', py', pz'] -> [px', py', pz', 1] -> [px, py, pz, 1]-> [px, py, pz]"""
        Pcam = np.array([P[0],P[1],P[2],1])
        Pecran = self.cToE@Pcam
        return Pecran[:3]

    def dirCamToEcran(self, P):
        """
        * Pas homogene
        !! Transforme des directions !! """
        return np.transpose(self.R)@P

    def camToCCD(self, C):
        """
        * homogene
        [px', py', pz', 1] -> [U,V,-F,1]
        """
        pzp=C[2]
        loic = np.block( [ [ np.eye(3) , np.zeros((3,1)).reshape(3,1) ],
                [np.zeros((1,3)).reshape(1,3) , -pzp/self.F]
                ])
        return -self.F/pzp*loic@C

    def spaceToPixel(self, vecSpace):
        """
        * homogene
        [U,V,-F,1] ->[u,v,1]

        Args:
        vecSpace: np.array([U,V,-F,1])
            Vecteur de position en m
        Returns:
            np.array([u,v,1])
            Vecteur de position en pixel
        """
        loic = np.block( [ self.K , np.zeros((3,1))] )
        vecPix = (-1/self.F)*loic@vecSpace
        u, v = vecPix[0], vecPix[1]
        # return np.array([u,v,1])

        if u > 1 and v > 1 and u < self.sgmf.shape[0]-1 and v < self.sgmf.shape[1]-1:

            if (self.mask[int(u),int(v),2] > 100):
               self.U.append(np.array([u,v]))
               return np.array([u,v,1])
            # if ( (u-self.centre_x)**2 + (v-self.centre_y)**2 < self.rayon**2 ):
            #     if np.abs( v - self.centre_y ) < np.sqrt(2)/2*self.rayon:
            #         self.U.append(np.array([u,v]))
            #         return np.array([u,v,1])
            else:
                # return np.array([0,0])
                return None
        else:
            return None


    def pixelToSpace(self, vecPix):
        """
        * homogene
        [u,v,1] -> [U,V-F,1]

        Prend la coordonnée d'un pixel de la caméra (u,v,1) [pixel] et le transforme en coordonnées dans le référentiel de la caméra (U,V,-F,1) [m]
        Args:
            vecPix : np.array([u,v,1])
            Vecteur de position en pixel
        Returns:
            vecSpace: np.array([U,V,-F,1])
            Vecteur de position en m
        """
        Kinv = np.array([[1/self.fx,-self.s/(self.fx*self.fy),self.s*self.cv/(self.fx*self.fy) - self.cu/self.fx],
                         [0,1/self.fy,-self.cv/self.fy],
                         [0,0,self.F],
                         [0,0,1]])
        vecSpace = Kinv@vecPix
        return vecSpace


    def pixCamToEcran(self, vecPix):

        """
        * homogene
        [u,v,1] -> [u',v',1]

        À partir des coordonées [u,v,1] (en pixels) d'un pixel de la caméra, donne le pixel d'écran correspondant [u',v',1] (en pixels)

        Args:
            vecPix : np.array([u,v,1])
            Coordonnées d'un point de la caméra en pixels
        Returns:
            np.array([u',v',1])
            Coordonnées d'un point de l'écran en pixels
        """

        uE = [int(np.floor(vecPix[0])), int(np.floor(vecPix[1]))] #entier
        uR = np.mod(vecPix,1) #reste

        up = self.sgmf[uE[0],uE[1],0] + uR[0]*( self.sgmf[uE[0]+1, uE[1]+1, 0] - self.sgmf[uE[0],uE[1],0] )
        vp = self.sgmf[uE[0],uE[1],1] + uR[1]*( self.sgmf[uE[0]+1, uE[1]+1, 1] - self.sgmf[uE[0],uE[1],1] )

        return np.array([up, vp, 1])

    def cacmouE(self, vecPix):
        """
        * Pas homogène
        [u,v,1] -> [X,Y,Z]

        Prend la coordonnée d'un pixel de la caméra (u,v,1) [pixel] et le transforme
        1) en coordonnées dans le référentiel de la caméra (U,V,-F,1) [m]
        2) en coordonnées dans le référentiel de l'écran (X,Y,Z) [m]
        Args:
            vecPix : np.array([u,v,1])
        Returns:
            np.array([X,Y,Z])
        """
        return self.camToEcran(self.pixelToSpace(vecPix)[0:3])

    def cacmouC(self, vecPix):
        """
        * Pas homogène
        [u,v,1] -> [U,V,-F]

        Prend la coordonnée d'un pixel de la caméra (u,v,1) [pixel] et le transforme en coordonnées dans le référentiel de la caméra (U,V,-F,1) [m]
        Args:
            vecPix : np.array([u,v,1])
        Returns:
            np.array([U,V,-F])
        """
        return self.pixelToSpace(vecPix)[0:3]
