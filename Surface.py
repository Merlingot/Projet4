class Point:

    def __init__(self, pmin, min, n1, n2):
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
    def ajouter_point(self, point):
        self.points.append(point)
        if len(self.points) > self.longueur :
            print('Erreur nombre de points sur la surface')
