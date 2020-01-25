""" Functions needed fot the search algorithm """
from Camera import Camera
from Ecran import Ecran
from Surface import Surface, Point
import seaborn as sns


import numpy as np
from numpy import abs
from numpy.linalg import norm
import matplotlib.pyplot as plt


def search(d, h, L, grid, precision, cam1, cam2, ecran):
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
    N=int(np.floor(L/h)) #nombre d'itérations (de descentes) pour un seul point
    surface=Surface(grid)
    for p in grid:
        p_initial = np.array([ p[0], p[1], p[2] ])
        n=0; bon=False
        p_min = p; min = 1e10 #(infini)
        V = np.zeros(N)
        while n<N:
            n+=1
            val, n1, n2, bon = evaluatePoint(p, cam1, cam2, ecran)
            # patate(p,cam1, cam2, n1, n2)
            V[n-1]=val
            if bon:
                if val < min:
                    min = val
                    p_min = np.array([p[0],p[1],p[2]])
            p += h*d #search ALONG d

        # Visualisation of SGMF points
        # if cam1.U != [] and cam2.U != []:
        #     f, (ax1, ax2, ax3) = plt.subplots(1, 3)
        #     ax1.imshow(cam1.sgmf[:,:,0], cmap="Greys", origin='lower')
        #     for pt in cam1.U:
        #         ax1.scatter( pt[0], pt[1], color='r')
        #     ax2.imshow(cam2.sgmf[:,:,0], cmap="Greys", origin='lower')
        #     for pt in cam2.U:
        #         ax2.scatter( pt[0], pt[1], color='r')
        #     ax3.plot(np.arange(0,N), V, 'b')
        #     plt.show()

        cam1.U = []
        cam2.U = []

        p_minus1 = p_min - h*d
        p_plus1 = p_min + h*d
        p_min, min, n1, n2 = ternarySearch(precision, p_minus1, p_plus1, cam1, cam2, ecran)
        if not (p_min[0] == p_initial[0]):
            surface.ajouter_point( Point(p_min, min, n1, n2) )

    return surface



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
        return m2(n1, n2), n1, n2, True #True:existe sur les caméras
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
    # Mettre P en coordonnées homogènes:
    p = np.array([P[0], P[1], P[2], 1]) #[px, py, pz, 1]

    # Mettre P dans le référentiel de la caméra
    C = cam.ecranToCam(p) #[px', py', pz', 1]
    # Prolonger jusqu'au CCD
    c = cam.camToCCD(C) #[U,V,F,1]
    # Mettre en pixel
    u = cam.spaceToPixel(c) #[u1,u2] # spaceToPixel est une fonction qui passe de position x,y sur l'écran de la caméra à des pixel
    if isinstance(u, np.ndarray):
        # Transformer un pixel sur la caméra à un pixel sur l'écran (SGMF)
        v = cam.pixCamToEcran(u) #[v1,v2]
        # Transformer de pixel au référentiel de l'écran
        e = ecran.pixelToSpace(v) #e=(x,y,1) # pixelToSpace est une fonction qui passe de pixel de l'écran à x,y sur l'écran
        E = np.array([e[0], e[1], 0])
        return normale(P,E,cam.S)
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



def getApproxZDirection(cam1, cam2):

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



def patate(P, cam1, cam2, n1, n2):

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

    C1=cam1.ecranToCam(P); c1=cam1.camToCCD(C1)
    d1=cam1.camToEcran(c1)-P
    ax.quiver(P[0],P[1],P[2], d1[0],d1[1],d1[2])

    C2=cam2.ecranToCam(P); c2=cam2.camToCCD(C2)
    d2=cam2.camToEcran(c2)-P
    # ----------------------------------------------------
    L=5e-2 #Longueur flêches

    ax.quiver(P[0],P[1],P[2], d2[0],d2[1],d2[2])
    ax.quiver(P[0],P[1],P[2], n1[0]*L,n1[1]*L,n1[2]*L, color='r')
    ax.quiver(P[0],P[1],P[2], n2[0]*L,n2[1]*L,n2[2]*L, color='g')

    dirCam1 = cam1.camToEcran(np.array([0,0,-1]))*L
    dirCam2 = cam2.camToEcran(np.array([0,0,-1]))*L
    ax.scatter(0,0,0)
    ax.scatter(cam1.S[0], cam1.S[1], cam1.S[2], marker='x')
    ax.scatter(cam2.S[0], cam2.S[1], cam2.S[2], marker='x')
    ax.quiver(0,0,0,0,0,L)
    # ax.quiver(t[0],t[1],t[2], d[0]*L,d[1]*L,d[2]*L)
    ax.quiver(cam1.S[0], cam1.S[1], cam1.S[2], dirCam1[0], dirCam1[1], dirCam1[2])
    ax.quiver(cam2.S[0], cam2.S[1], cam2.S[2], dirCam2[0], dirCam2[1], dirCam2[2])

    plt.show()
















#
