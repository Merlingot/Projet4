import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage.io import imread, imsave
# import seaborn as sns


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
    def __init__(self, ecran, K, R, T, W, sgmf):

        # Setup
        self.ecran = ecran

        ## SGMF
        #Importing cartography
        sgmfXY = cv2.imread(sgmf).astype('float64') #SHAPE (Y,X,RGB)
        # sgmfXY = cv2.bilateralFilter(sgmfXY, 7, sigmaSpace = 75, sigmaColor =75)

        #Importing confidence mask
        # self.mask = cv2.imread(mask).astype('int')

        #Green channel
        self.sgmf = np.zeros( (sgmfXY.shape[0], sgmfXY.shape[1], sgmfXY.shape[2]-1) )
        self.sgmf[:,:,0] = sgmfXY[:,:,1] * self.ecran.w[0] / 255.
        self.sgmf[:,:,1] = sgmfXY[:,:,2] * self.ecran.w[1] / 255.

        # self.U = []

        # Intrinsèque
        self.K = K                              # Tout information
        self.fx=K[0,0]; self.fy=K[1,1]
        self.cu=K[0,2]; self.cv=K[1,2]
        self.f = ( self.fx + self.fy ) / 2.     # Focale camera [f]=pixels
        self.c = np.array([self.cu, self.cv])   # Centre optique du CCD [c]=pix
        self.s = K[0,1]                         # Skew
        self.W = W                              # Taille du CCD en [W]=m
        self.w = np.array([sgmfXY.shape[1],sgmfXY.shape[0]])                             # Taille du CCD en [w]=pixels

        # BINNING ???????
        self.sx = self.W[0]/self.w[0]                     # Taille d'un pixel [m/pixel]
        self.sy = self.W[1]/self.w[1]                     # Taille d'un pixel [m/pixel]

        self.F = ( self.fx*self.sx + self.fy*self.sy ) / 2. #Focale utile [m]

        # Extrinsèque (Ecran -> Camera)
        self.R = R                              # Matrice de rotation [-]
        self.T = T                              # Matrice de translation [m]

        # Matrices de Passage
        self.eToC = np.block([ [R , T.reshape(3,1)] ,
                [ np.zeros((1,3)).reshape(1,3) , 1]
                ])
        self.cToE = np.block([ [np.transpose(R) , -(np.transpose(R)@T).reshape(3,1)] ,
                [ np.zeros((1,3)).reshape(1,3) , 1]
                ])

        self.Khom = np.block( [ self.K , np.zeros((3,1))] )
        self.Kinv = np.array([[1/self.fx,-self.s/(self.fx*self.fy),self.s*self.cv/(self.fx*self.fy) - self.cu/self.fx],
                         [0,1/self.fy,-self.cv/self.fy],
                         [0,0,1],
                         [0,0,-1/self.F]])

        # Position du sténopé de la caméra dans le référentiel de l'écran
        self.S = self.camToEcran( np.array( [0,0,0,1]) )
        # Normale de la caméra dans le référentiel de l'écran
        self.normale = self.camToEcran( np.array([0,0,1,0]))


    def ecranToCam(self, P):
        """
        * homogene
        [px, py, pz, 1] -> [px', py', pz', 1] """
        return self.eToC@P

    def camToEcran(self, P):
        """
        * homogene
        [px', py', pz', -] -> [px, py, pz, -]"""
        return self.cToE@P

    def camToCCD(self, C):
        """
        * homogene
        [px', py', pz', 1] -> [U,V,-F,1]
        """
        pzp=C[2]
        mat = np.block( [ [ np.eye(3) , np.zeros((3,1)).reshape(3,1) ],
                        [np.zeros((1,3)).reshape(1,3) , -pzp/self.F]
                        ])
        return -self.F/pzp*mat@C

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
        vecPix = (-1/self.F)*self.Khom@vecSpace
        u, v = vecPix[0], vecPix[1]
        if u >= 1 and v >= 1 and u < self.sgmf.shape[1] and v < self.sgmf.shape[0]:
            if (self.mask[int(v),int(u)] == True):
                return np.array([u,v,1])
            else:
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
            np.array([U,V,-F,1])
            Vecteur de position en m
        """
        return -self.F*self.Kinv@vecPix


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

        up = self.sgmf[uE[1],uE[0],0]
        # + uR[1]*( self.sgmf[uE[1]+1, uE[0]+1, 0] - self.sgmf[uE[1],uE[0],0] )
        vp = self.sgmf[uE[1],uE[0],1]
        # + uR[0]*( self.sgmf[uE[1]+1, uE[0]+1, 1] - self.sgmf[uE[1],uE[0],1] )

        return np.array([up, vp, 1])

    def cacmouE(self, vecPix):
        """
        * homogène (fonction d'affichage)
        [u,v,1] -> [X,Y,Z,1]

        Prend la coordonnée d'un pixel de la caméra (u,v,1) [pixel] et le transforme
        1) en coordonnées dans le référentiel de la caméra (U,V,-F,1) [m]
        2) en coordonnées dans le référentiel de l'écran (X,Y,Z,1) [m]
        Args:
            vecPix : np.array([u,v,1])
        Returns:
            np.array([X,Y,Z,1])
        """
        return self.camToEcran( self.pixelToSpace(vecPix) )

    def cacmouC(self, vecPix):
        """
        * homogène (fonction d'affichage)
        [u,v,1] -> [U,V,-F,1]

        Prend la coordonnée d'un pixel de la caméra (u,v,1) [pixel] et le transforme en coordonnées dans le référentiel de la caméra (U,V,-F,1) [m]
        Args:
            vecPix : np.array([u,v,1])
        Returns:
            np.array([U,V,-F,1])
        """
        return self.pixelToSpace(vecPix)
