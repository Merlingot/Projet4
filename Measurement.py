class Ecran:

    def __init__(self):

        self.x=None
        self.y=None
        self.n=None

        self.dis_x=None
        self.dis_y=None

class Camera:

    def __init__(self):

        self.I=None 
        self.cx=None
        self.cy=None



class Measurement:
    
    def __init__(self):
        
        self.pos_camera=None
        self.pos_ecran=None
        self.pos_stenope=None

        self.sgmf=None 

    def normale(p):

        #trouver vec de p a s
        PS = self.pos_stenope - p
        # 

        


