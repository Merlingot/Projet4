""" Functions needed fot the search algorithm """
from Camera import Camera
from Ecran import Ecran
from Surface import Surface, Point
# import seaborn as sns
from util import show_sgmf


import numpy as np
from numpy import abs
from numpy.linalg import norm
import matplotlib.pyplot as plt



def search(surface, d, h, L, precision, cam1, cam2, ecran):
    """
    Find the position (vector p_min) and value (min) of the minimum on each point of the grid
    Args:
        d (np.array([x,y,z])) : direction de recherche (vecteur unitaire)
        h (float) : incrément de recherche
        grid (list[np.array([x,y,z])]) :
        precision (float) :
        cam1, cam2 : caméra
        ecran : ecran
    Return:
        Objet surface
    """
    N=int(np.floor(L/h)) # nombre d'itérations (de descentes) pour un seul point
    i=0 # index pour les points
    for p in surface.grid:
        p_initial = np.array([ p[0], p[1], p[2] ])
        n=0; bon=False
        p_min = p_initial; min = 1e10 #(infini)
        V = np.zeros(N)
        while n<N:
            n+=1
            val, n1, n2, bon = evaluatePoint(p, cam1, cam2, ecran)
            V[n-1]=val
            if bon:
                if val < min:
                    min = val
                    p_min = np.array([p[0],p[1],p[2]])
            p += h*d #search ALONG d

        # show_sgmf(cam1, cam2,N,V,h)
        cam1.U = []
        cam2.U = []

        p_minus1 = p_min - h*d
        p_plus1 = p_min + h*d
        p_min, min, n1, n2 = ternarySearch(precision, p_minus1, p_plus1, cam1, cam2, ecran)

        # Enregistrer le point étudié
        surface.ajouter_point(Point(p_initial, p_min, min, n1, n2))
        # Enregistrer la position finale du point étudié en format vecteur
        surface.x_f[i]=p_min[0]; surface.y_f[i]=p_min[1]; surface.z_f[i]=p_min[2];
        i+=1


def evaluatePoint(p, cam1, cam2, ecran):
    """
    Evaluate the inconsistensy m of two measurements from cam1 and cam2 at a point p
    Args:
        p = np.array([x,y,z])
        cam1, cam2 : measurements nb. 1 and 2
    Returns:
        Inconsistensy, two normals
    """
    P = homogene(p)

    n1 = normal_at(P, cam1, ecran); n2 = normal_at(P, cam2, ecran)

    if isinstance(n1, np.ndarray) and isinstance(n2, np.ndarray) :
        return m1(n1, n2), cartesienne(n1), cartesienne(n2), True #True:existe sur les caméras
    else:
        return None, None, None, False

def normal_at(P, cam, ecran):
    """
    *homogene
    Évaluer la normale en un point p
    Args:
        P : np.array([x,y,z,1])
            Point dans le référentiel de l'écran, homogène
        cam: Structure Camera
            Caméra qui regarde le point
        ecran : Structure écran
            Écran qui shoote des pattern
    returns
        n = np.array([x,y,z,0]) (unit vector)
    """

    # Mettre P dans le référentiel de la caméra
    C = cam.ecranToCam(P) #[px', py', pz', 1]
    # Prolonger jusqu'au CCD
    c = cam.camToCCD(C) #[U,V,-F,1]
    # Mettre en pixel
    u = cam.spaceToPixel(c) #[u1,u2,1]
    if isinstance(u, np.ndarray):
        # Transformer un pixel sur la caméra à un pixel sur l'écran (SGMF)
        vecPix = cam.pixCamToEcran(u) #[v1,v2,1]
        # Transformer de pixel au référentiel de l'écran
        E = ecran.pixelToSpace(vecPix) #[x,y,0] # pixelToSpace est une fonction qui passe de pixel de l'écran à x,y sur l'écran
        return normale(P, homogene(E), homogene(cam.S))
    else:
        return None


# - Fonctions qui handles pas les None ------------------------------

def homogene(vec):
    """ np.array([x,y,z]) -> np.array([x,y,z,1])   """
    if vec.size == 3:
        return np.array([vec[0], vec[1], vec[2], 1])
    else:
        return vec

def cartesienne(vec_hom):
    """ np.array([x,y,z,1]) - > np.array([x,y,z]) """
    if vec_hom.size == 4:
        return np.array([vec_hom[0], vec_hom[1], vec_hom[2]])
    else:
        return vec_hom

def normale(P,E,C):
    """
    *homogene
    Calculer une normale avec 3 points dans le même référentiel
    P:point E:écran C:caméra (x,y,z,1)
    """
    PE = E-P; PC = C-P
    pe = PE/np.linalg.norm(PE); pc = PC/np.linalg.norm(PC)
    N = pe + pc
    n = N/np.linalg.norm(N)
    return n

def m1(n1, n2):
    """
    *homogene
    Inconsistensy of the current point p.
    Definition: m=1-absolute_value( n1<dot_product>n2 )
    Args:
        n1, n2 : np.array([x,y,z,0])
    """
    return 1 - np.abs(n1@n2)

def m2(n1, n2):
    """
    *homogene
    Inconsistensy of the current point p.
    Definition : m=n1<cross_product>n2
    Args:
        n1, n2 : np.array([x,y,z,0])"""
    return norm(np.cross(n1, n2))

def ternarySearch(absolutePrecision, lower, upper, cam1, cam2, ecran):
    """
    Find the maximum in the interval [<lower>, <upper>] with a precision of <absolutePrecision>.
    Recursive function.
    Args:
        absolutePrecision : float
            Precision of the search interval
        lower : np.array([x,y,z])
            Current lower bound of search domain
        upper : np.array([x,y,z])
            Current upper bound of search domain
        cam1, cam2 : Caméra
            Measurements nb. 1 and 2
    Return:
        p_min : np.array([x,y,z])
        min :
    """
    p_min = (lower + upper)/2
    min, n1, n2, _ = evaluatePoint(p_min, cam1, cam2, ecran)
    return p_min, min, n1, n2



def getApproxZDirection(cam1, cam2):

    """ Donne la direction approximative de la table dans le référentiel de l'écran"""

    zE_E = np.array([0,0,-1])
    zC_C = np.array([0,0,1])
    zC1_E = cam1.camToEcran(zC_C)
    zC1_E /= np.linalg.norm(zC1_E)
    zC2_E = cam2.camToEcran(zC_C)
    zC2_E /= np.linalg.norm(zC2_E)

    z1_E = zE_E + zC1_E; z1_E /=np.linalg.norm(z1_E)
    z2_E = zE_E + zC2_E; z2_E /=np.linalg.norm(z2_E)
    return (z1_E + z2_E)/2

def graham(v1, v2, v3):
    """
    Find the orthogonal basis with direction v1 as d
    Args:
    Return:
    """
    u1 = v1
    e1 = u1/np.linalg.norm(u1)
    u2 = v2 - ( np.dot(u1, v2) / np.dot(u1,u1) ) * u1
    e2 = u2/np.linalg.norm(u2)
    u3 = v3 - ( np.dot(u1, v3) / np.dot(u1,u1) ) * u1 - ( np.dot(u2, v3) / np.dot(u2,u2) ) * u2
    e3 = u3/np.linalg.norm(u3)

    return np.concatenate((e1,e2,e3), axis=0).reshape(3,3)













#
