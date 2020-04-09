import numpy as np

class Point:

    def __init__(self, p_initial, pmin, min, n1, n2):
        self.p_initial=p_initial
        self.pmin=pmin
        self.inconsistensy=min
        self.n1=n1
        self.n2=n2
        self.pix_ccd=None
        self.pix_ecran=None
        self.sgmf_confirmed=False


class Surface:

    def __init__(self, grid):
        self.grid=grid
        self.points=[]
        self.longueur=len(grid) #Nombre de point dans la grille
        # Points initiaux de la grille
        self.x_i=np.zeros(self.longueur); self.y_i=np.zeros(self.longueur); self.z_i=np.zeros(self.longueur)
        # Points finaux de la grille
        self.x_f=np.zeros(self.longueur); self.y_f=np.zeros(self.longueur); self.z_f=np.zeros(self.longueur)
        self.enr_points_initiaux()

    def ajouter_point(self, point):
        self.points.append(point)
        if len(self.points) > self.longueur :
            print('Erreur nombre de points sur la surface')

    def enr_points_initiaux(self):
        i=0
        for p in self.grid:
            p_initial = np.array([ p[0], p[1], p[2] ])
            # Enregistrer le point étudié (position initiale et finale) en format vecteur
            self.x_i[i]=p_initial[0]; self.y_i[i]=p_initial[1]; self.z_i[i]=p_initial[2]
            i+=1
