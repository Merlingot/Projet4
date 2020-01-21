""" Functions needed fot the search algorithm """
from Camera import Camera
from Ecran import Ecran
from Surface import Surface, Point
import seaborn as sns


import numpy as np
from numpy import abs
from numpy.linalg import norm
import matplotlib.pyplot as plt


def search(d, h, grid, precision, cam1, cam2, ecran):
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
    N=19 #nombre d'itérations (de descentes) pour un seul point
    surface=Surface(grid)
    for p in grid:
        n=0; bon=False
        p_min = p; min = 1e10 #(infini)
        V = np.zeros(N)
        while n<N:
            n+=1
            patate(p,cam1, cam2)
            val, n1, n2, bon = evaluatePoint(p, cam1, cam2, ecran)
            if bon:
                if val < min:
                    min = val
                    p_min = np.array([p[0],p[1],p[2]])
            p -= h*d #search along d

        # Visualisation of SGMF points
        #axy = sns.heatmap(cam1.sgmf[:,:,0], cmap="cool")

        b=False
        for pt in cam1.U:
            if(pt[0] + pt[1] != 0):
                b=True

        if (b):
            plt.figure()
            for pt in cam1.U:
                plt.scatter( pt[0], pt[1])
            plt.show()

        cam1.U = []
        cam2.U = []

        p_minus1 = p_min - h*d
        p_plus1 = p_min + h*d
        p_min, min, n1, n2 = ternarySearch(precision, p_minus1, p_plus1, cam1, cam2, ecran)
        surface.ajouter_point( Point(p_min, min, n1, n2) )
    return surface

def patate(P, cam1, cam2):

    fig=plt.figure()
    ax = fig.gca(projection='3d')
    ax.auto_scale_xyz([0, 1], [0, 1], [0, 1])

    ## Set aspect -----------------------------------------
    X=np.array([0, cam1.S[0]*1.3])
    Y=np.array([0, cam1.S[1]*1.3])
    Z=np.array([0, cam1.S[2]*1.3])
    # Create cubic bounding box to simulate equal aspect ratio
    max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
    Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
    Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
    Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())
    # Comment or uncomment following both lines to test the fake bounding box:
    for xb, yb, zb in zip(Xb, Yb, Zb):
       ax.plot([xb], [yb], [zb], 'w')
    ## Set aspect -----------------------------------------

    d1=cam1.S-P
    ax.quiver(P[0],P[1],P[2], d1[0],d1[1],d1[2])

    d2=cam2.S-P
    ax.quiver(P[0],P[1],P[2], d2[0],d2[1],d2[2])

    # ----------------------------------------------------
    L=5e-2 #Longueur flêches
    dirCam1 = np.dot(cam1.R, np.array([0,0,-1]))*L
    dirCam2 = np.dot(cam2.R, np.array([0,0,-1]))*L
    ax.scatter(0,0,0)
    ax.scatter(cam1.S[0], cam1.S[1], cam1.S[2], marker='x')
    ax.scatter(cam2.S[0], cam2.S[1], cam2.S[2], marker='x')
    ax.quiver(0,0,0,0,0,L)
    # ax.quiver(t[0],t[1],t[2], d[0]*L,d[1]*L,d[2]*L)
    ax.quiver(cam1.S[0], cam1.S[1], cam1.S[2], dirCam1[0], dirCam1[1], dirCam1[2])
    ax.quiver(cam2.S[0], cam2.S[1], cam2.S[2], dirCam2[0], dirCam2[1], dirCam2[2])

    plt.show()



def evaluatePoint(P, cam1, cam2, ecran):
    """
    Evaluate the inconsistensy m of two measurements from cam1 and cam2 at a point p
    Args:
        P = np.array([x,y,z])
        cam1, cam2 : measurements nb. 1 and 2
    Returns:
        Inconsistensy, two normals
    """
    n1 = normal_at(P, cam1, ecran); n2 = normal_at(P, cam2, ecran)

    if isinstance(n1, np.ndarray) and isinstance(n2, np.ndarray) :
        return m1(n1, n2), n1, n2, True #True:existe sur les caméras
    else:
        return None, None, None, False

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
    C = cam.R@P + cam.T #[X,Y,Z]
    # Écraser Pc dans le référentiel 2D de la caméra
    c = cam.F/C[2]*C[0:2] #[x,y]
    # Mettre en pixel
    u = cam.spaceToPixel(c) #[u1,u2] # spaceToPixel est une fonction qui passe de position x,y sur l'écran de la caméra à  des pixel
    # Transformer un pixel sur la caméra à un pixel sur l'écran
    v = cam.pixCamToEcran(u) #[v1,v2]
    if isinstance(v, np.ndarray):
        # Transformer de pixel au référentiel de l'écran
        e = ecran.pixelToSpace(v) #e=(x,y) # pixelToSpace est une fonction qui passe de pixel de l'écran à x,y sur l'écran
        E = np.array([e[0], e[1], 0])
        S = np.linalg.inv(cam.R)@(-cam.T)
        return normale(P,E,S)
    else:
        return None


# - Fonctions qui handles pas les None ------------------------------
def normale(P,E,C):
    """ Calculer une normale avec 3 points dans le même référentiel
    P:point E:écran C:caméra
    """
    PE = E-P; PC = C-P
    pe = PE/np.linalg.norm(PE); pc = PC/np.linalg.norm(PC)
    N = pe + pc
    n = N/np.linalg.norm(N)
    return n

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

    ## PROBLEME DANS CETTE FONCTION!
    # # Note : upper = lower+c*d with d the search direction.
    # if abs(norm(upper - lower)) < absolutePrecision:
    #     p_min = (lower + upper)/2
    #     min, n1, n2, _ = evaluatePoint(p_min, cam1, cam2, ecran)
    #     return p_min, min, n1, n2
    # lowerThird = (2*lower + upper)/3
    # upperThird = (lower + 2*upper)/3
    #
    # # PAS bon ça : compare tuple avec tuple
    # if evaluatePoint(lowerThird, cam1, cam2, ecran) < evaluatePoint(upperThird,  cam1, cam2, ecran):
    #     ternarySearch(absolutePrecision, lowerThird, upper, cam1, cam2, ecran)
    # else:
    #     ternarySearch(absolutePrecision, lower, upperThird, cam1, cam2, ecran)


# def getApproxZDirection(R1, R2):
#
#     zEcran = np.array([0, 0, 1])
#
#     zCam1 = np.dot( R1, np.transpose(zEcran) )
#     zCam1 /= np.linalg.norm(zCam1)
#     zCam2 = np.dot( R2, np.transpose(zEcran) )
#     zCam2 /= np.linalg.norm(zCam2)
#
#     zDirection1 = zEcran + zCam1
#     zDirection1 /= np.linalg.norm(zDirection1)
#     zDirection2 = zEcran + zCam2
#     zDirection2 /= np.linalg.norm(zDirection2)
#
#     zDirApprox = zDirection1 + zDirection2
#
#     return zDirApprox / np.linalg.norm(zDirApprox)


def getApproxZDirection(cam1, cam2):

    zE_E = np.array([0,0,-1])
    zC_C = np.array([0,0,1])
    zC1_E = np.linalg.inv(cam1.R)@(zC_C)
    zC1_E=zC1_E/np.linalg.norm(zC1_E)
    zC2_E = np.linalg.inv(cam2.R)@(zC_C)
    zC2_E=zC2_E/np.linalg.norm(zC2_E)
    # print(zC1_E, zC2_E)

    z1_E = zE_E + zC1_E
    z2_E = zE_E + zC2_E
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
