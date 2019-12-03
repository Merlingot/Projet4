""" Functions needed fot the search algorithm """
from Camera import Camera
from Ecran import Ecran

import numpy as np
from numpy import abs
from numpy.linalg import norm


def search(t, grid, precision, V, cam1, cam2, ecran):
    """
    Find the position (vector p_min) and value (min) of the minimum on each point of the grid
    Args:
        t (float) : search step
        grid (list[np.array([x,y,z])]) :
        precision (float) :
        V (np.array([x,y,z])) : Volume
        cam1, cam2 : caméra
        ecran : ecran
    Return:
        rv: list(list(p_min, min)) -> fire un objet
        TO DO ajouter les normales, dezip
    """
    rv=[]
    for p in grid:
        p_min = p
        min = 10e100 #(infini)
        while p[2]<=V[2]:
            val = evaluatePoint(p, cam1, cam2)
            if val < min:
                min = val
                p_min = p
            p += t*d #search along d
        p_minus1 = p_min - t*d
        p_plus1 = p_min + t*d
        p_min, min  = ternarySearch(precision, p_minus1, p_plus1, cam1, cam2)
        rv.append([p_min, min])
    return rv

def ternarySearch(absolutePrecision, lower, upper, cam1, cam2):
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
    # Note : upper = lower+c*d with d the search direction.
    # Everything works with vectors
    if abs(norm(upper - lower)) < absolutePrecision:
        p_min = (lower + upper)/2
        min = evaluatePoint(p_min, D1, D2)
        return p_min, min
    lowerThird = (2*lower + upper)/3
    upperThird = (lower + 2*upper)/3

    if evaluatePoint(lowerThird, D1, D2) < evaluatePoint(upperThird,  D1, D2):
        ternarySearch(absolutePrecision, lowerThird, upper, D1, D2)
    else:
        ternarySearch(absolutePrecision, lower, upperThird, D1, D2)


def m1(n1, n2):
    """Inconsistensy of the current point p.
    Definition: m=1-absolute_value( n1<dot_product>n2 )
    Args:
        n1, n2 : np.array([x,y,z])
    """
    return 1 - np.abs(n1@n2)

def m2(n1, n2):
    """Inconsistensy of the current point p.
    Definition : m=n1<cross_product>n2
    Args:
        n1, n2 : np.array([x,y,z])"""
    return norm(np.cross(n1, n2))


def evaluatePoint(p, D1, D2):
    """
    Evaluate the inconsistensy m of two measurements D1 and D2 at a point p
    Args:
        p = np.array([x,y,z])
        D1, D2 : measurements nb. 1 and 2
    Returns:
        Inconsistensy
    """
    n1 = normal_at(p, D1)
    n2 = normal_at(p,D2)
    return m1(n1, n2)



def normal_at(P, cam, ecran):
    """
    Évaluer la normale en un point p
    Args:
        P : np.array([x,y,z])
            Point dans le référentiel de l'écran
        cam: Structure Camera
            Caméra qui regarde le point
        ecran : Structure écran
            Écran qui shoote des pattern
    returns
        n = np.array([x,y,z]) (unit vector)
    """

    # Mettre P dans le référentiel de la caméra
    C = (cam.R + cam.T)@P #[X,Y,Z]
    # Écraser Pc dans le référentiel de l'écran
    c = cam.F/P[2]*C[0:1] #[x,y]
    # Mettre en pixel
    u = cam.spaceToPixel(c) #[u1,u2]
    #Kc est une fonction qui passe de position x,y sur l'écran de la caméra à  des pixel
    # Pixel sur l'écran
    v = cam.sgmf(u) #[e1,e2]
    # Transformer de pixel au référentiel de l'écran
    e = ecran.pixelToSpace(e) #e=(x,Yy)
    #Ke est une fonction qui passe de pixel de l'écran à x,y sur l'écran
    E = np.array([e[0], e[1], 0])
    return normale(P,E,C)


def normale(P,E,C):
    """ Calculer une normale avec 3 points dans le même référentiel """
    PE = E-P; PC = C-P
    pe = PE/np.norm(PE); pc = PC/np.norm(PC)
    N = pe + pc
    n = N/np.norm(N)
    return n


































#
