class Point:

    def __init__(self, pmin, min, n1, n2):
        self.xyz=pmin
        self.inconsistensy=min
        self.n1=n1
        self.n2=n2



class Surface:

    def __init__(self, grid):
        self.points=[]
        self.longueur=len(grid)
    def ajouter_point(self, point):
        self.points.append(point)
        if len(self.points) > self.longueur :
            print('Erreur nombre de points sur la surface')
