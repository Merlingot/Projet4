import numpy as np

class Point:

    def __init__(self, p_initial, pmin, min, n1, n2):
        self.p_initial=p_initial
        self.xyz=pmin
        self.inconsistensy=min
        self.n1=n1
        self.n2=n2
        self.pix_ccd=None
        self.pix_ecran=None
        self.sgmf_confirmed=False


class Surface:

    def __init__(self, grid):
        self.points=[]
        self.longueur=len(grid) #Nombre de point dans la grille
        # Points initiaux de la grille
        self.x_i=np.zeros(self.longueur); self.y_i=np.zeros(self.longueur); self.z_i=np.zeros(self.longueur)
        # Points finaux de la grille
        self.x_f=np.zeros(self.longueur); self.y_f=np.zeros(self.longueur); self.z_f=np.zeros(self.longueur)

    def ajouter_point(self, point):
        self.points.append(point)
        if len(self.points) > self.longueur :
            print('Erreur nombre de points sur la surface')
