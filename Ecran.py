import numpy as np



class Ecran:

    def __init__(self, W, w):
        """
        W = np.array([W,Wy]) # [m]
        w = np.array([wx,wy]) # [pixel]
        """
        self.W=W
        self.w=w

        alpha_x = W[0]/w[0]; alpha_y = W[1]/w[1]

        self.loic = np.zeros((3,3))
        self.loic[0,0]=alpha_x; self.loic[1,1]=alpha_y

    def pixelToSpace(self, vecPix):
        """
        * homogene
        Args:
        vecPix: np.array([u',v',1])
            Vecteur de position en pixels
        Returns:
            np.array([x,y,0])
            Vecteur de position en m
        """
        return self.loic@vecPix
