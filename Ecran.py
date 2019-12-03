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

    def pixelToSpace(vecPix):
        """
        Args:
        vecPix: np.array([u,v])
            Vecteur de position en pixels
        Returns:
            np.array([x,y])
            Vecteur de position en m
        """
        u,v = vecPix[0], vecPix[1]
        x,y = (u - self.cx)/self.sx, (v-self.cy)/self.sy
        return np.array([x,y])
