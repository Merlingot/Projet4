import numpy as np



class Ecran:

    def __init__(self, W, w, c):
        """
        W = np.array([W,Wy]) # [m]
        w = np.array([wx,wy]) # [pixel]
        c = np.array([cx,cy]) # [pixel]
        """
        self.W = W
        self.w = w
        self.c =c

        self.sx = w[0]/W[0]
        self.sy = w[1]/W[1]

    def pixelToSpace(self, vecPix):
        """
        Args:
        vecPix: np.array([ux,uy])
            Vecteur de position en pixels
        Returns:
            np.array([x,y])
            Vecteur de position en m
        """
        ux,uy = vecPix[0], vecPix[1]
        x,y = (ux - self.c[0])/self.sx, (uy-self.c[1])/self.sy
        return np.array([x,y])
