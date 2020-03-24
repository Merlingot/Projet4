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
        self.c=np.array([c[0],c[1],1])

        # Facteur de conversion
        alpha_x = W[0]/w[0]; alpha_y = W[1]/w[1]  # m/pixel

        # Matrice de passage [u',v',1] -> [X,Y,0]
        self.M = np.eye((3,3))
        self.M[0,0]=alpha_x; self.M[1,1]=alpha_y
        # Matrice de passage [X,Y,0] -> [u',v',1]
        self.Minv = np.eye((3,3))
        self.Minv[0,0]=1/alpha_x; self.Minv[1,1]=1/alpha_y

    def pixelToSpace(self, vecPix):
        """
        * homogene en entrée
        Args:
        vecPix: np.array([u',v',1])
            Vecteur de position en pixels de l'écran
        Returns:
            np.array([X,Y,0])
            Vecteur de position en m sur l'écran
        """
        return self.M@(vecPix - self.c)

    def spaceToPixel(self, vecSpace):
        """
        * homogene en sortie
        Args:
        vecSpace: np.array(X,Y,0])
            Vecteur de position en m sur l'écran
        Returns:
            np.array([u',v',1])
            Vecteur de position en pixels de l'écran
        """
        return self.Minv@vecSpace + self.c
