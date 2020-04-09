import numpy as np



class Ecran:

    def __init__(self, W, w, c):
        """
        W = np.array([Wx,Wy]) # [W]=m
        w = np.array([wx,wy]) # [w]=pixel
        c = np.array([cu,cv]) # [c]=pixel
        """
        self.W=W
        self.w=w
        self.c=c

        # Facteur de conversion
        alpha_x = W[0]/w[0]; alpha_y = W[1]/w[1]  # m/pixel
        cu = c[0]; cv = c[1] # pixel

        # Matrice de passage [u',v',1] -> [X,Y,0,1]
        self.M = np.array([[alpha_x,0,-alpha_x*cu],[0,alpha_y,-alpha_y*cv],[0,0,0],[0,0,1]])
        # Matrice de passage [X,Y,0,1] -> [u',v',1]
        self.Minv = np.array([[1/alpha_x,0,0,cu],[0,1/alpha_y,0,cv],[0,0,0,1]])


    def pixelToSpace(self, vecPix):
        """
        * homogene
        Args:
        vecPix: np.array([u',v',1])
            Vecteur de position en pixels de l'écran
        Returns:
            np.array([X,Y,0,1])
            Vecteur de position en m sur l'écran
        """
        return self.M@vecPix

    def spaceToPixel(self, vecSpace):
        """
        * homogene
        Args:
        vecSpace: np.array(X,Y,0,1])
            Vecteur de position en m sur l'écran
        Returns:
            np.array([u',v',1])
            Vecteur de position en pixels de l'écran
        """
        return self.Minv@vecSpace
