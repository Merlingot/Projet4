class Point:

    def __init__(self, pmin, min, n1, n2):
        self.xyz=pmin
        self.inconsistensy=min
        self.n1=n1
        self.n2=n2

class Surface:

    def __init__(self):
        self.points=[]
    def ajouter_point(self, point):
        index=len(self.points)
        self.points[index]=point
