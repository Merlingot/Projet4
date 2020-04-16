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



def search(surface, d, h, L, cam1, cam2, ecran):
    """
    Find the position (vector p_min) and value (min) of the minimum on each point of the grid
    Args:
        d (np.array([x,y,z])) : direction de recherche (vecteur unitaire)
        h (float) : incrément de recherche
        grid (list[np.array([x,y,z])]) :
        cam1, cam2 : caméra
        ecran : ecran
    Return:
        Objet surface
    """
    N=int(np.floor(L/h)) # nombre d'itérations (de descentes) pour un seul point
    for p in surface.grid: # Loop sur les points
        # print('------------------ POINT ----------------')
        point = Point(N)
        n=0; index_min=None; n_min=None
        p_initial = np.array([ p[0], p[1], p[2] ])
        p_min = np.array([ p[0], p[1], p[2] ]); val_min = 1e10 #(infini)
        while n<N: # Loop sur la descente du point
            b, val, n1, u1, e1, n2, u2, e2 = evaluatePoint(p, cam1, cam2, ecran)
            if b:
                if val < val_min:
                    index_min = n
                    val_min = val
                    p_min = np.array([p[0],p[1],p[2]])
                    n_min=(n1+n2)/2
            point.vecV[n]=val; point.vecP[n]=p; point.vecB[n]=b; point.vecN1[n]=n1; point.vecN2[n]=n2
            point.vecU1[n]=u1; point.vecE1[n]=e1;
            point.vecU2[n]=u2; point.vecE2[n]=e2;
            p += h*d
            n+=1

        # Enregistrer les valeurs minimales du point
        point.pmin=p_min; point.valmin=val_min; point.indexmin=index_min
        point.nmin=n_min
        # Arranger les vecteur pour enlever les NaN:
        point.vecV=point.vecV[point.vecB]
        point.vecP=point.vecP[point.vecB]
        point.vecN1 = point.vecN1[point.vecB];
        point.vecU1 = point.vecU1[point.vecB];
        point.vecE1 = point.vecE1[point.vecB];
        point.vecN2 = point.vecN2[point.vecB];
        point.vecU2 = point.vecU2[point.vecB];
        point.vecE2 = point.vecE2[point.vecB];
        # Enregistrer le point étudié seulement si au moins un bon point:
        if point.indexmin:
            surface.ajouter_point(point)
            # show_sgmf(cam1, cam2, point)

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

    n1, u1, e1 = normal_at(P, cam1, ecran); n2, u2, e2 = normal_at(P, cam2, ecran)

    if isinstance(n1, np.ndarray) and isinstance(n2, np.ndarray) :
        return True, m1(n1, n2), cartesienne(n1), u1, e1, cartesienne(n2), u2, e2
    else:
        return False, None, None, None, None, None, None, None

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
        E = ecran.pixelToSpace(vecPix) #[x,y,0,1] # pixelToSpace est une fonction qui passe de pixel de l'écran à x,y sur l'écran
        return normale(P, E, cam.S), u, vecPix
    else:
        return None, None, None

def homogene(vec):
    """ np.array([x,y,z]) -> np.array([x,y,z,1])   """
    if vec.size == 3:
        return np.array([vec[0], vec[1], vec[2], 1])
    else:
        return vec

def cartesienne(vec):
    """ np.array([x,y,z,-]) - > np.array([x,y,z]) """
    if vec.size == 4:
        return np.array([vec[0], vec[1], vec[2]])
    else:
        return vec

def normale(P,E,C):
    """
    *homogene
    Calculer une normale avec 3 points dans le même référentiel
    P:point E:écran C:caméra np.array([x,y,z,1])
    """
    r = P-E; p = P-C # r = vec(EP), p = vec(CP)
    r = r/np.linalg.norm(r); p = p/np.linalg.norm(p)
    n = - r - p
    n = n/np.linalg.norm(n)
    return n

def m2(n1, n2):
    """
    *homogene
    Inconsistensy of the current point p.
    Definition: m=1-absolute_value( n1<dot_product>n2 )
    Args:
        n1, n2 : np.array([x,y,z,0])
    """
    return 1 - np.abs(n1@n2)

def m1(n1, n2):
    """
    *homogene
    Inconsistensy of the current point p.
    Definition : m=n1<cross_product>n2
    Args:
        n1, n2 : np.array([x,y,z,0])"""

    return norm(np.cross(n1[:3], n2[:3]))


# Autre fonctions ------------------
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
