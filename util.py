import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import numpy as np
import plotly.figure_factory as ff



def fleche(vecI, vecDir, rgb=(0,0,0), s=1/10, l=1):
    """
    vecI : np.array([x,y,z])
        coordonées du point de départ de la flèche
    vecDir : np.array([x,y,z])
        vecteur unitaire donnant la direction du vecteur
    scale : nombre entre 0 et 1
        grossit ou diminue la dimension du cone
    l : nombre > 0
        longueur de la tige de la flèche
    rgb : tuple (r,g,b)
        code rgb de la couleur de la flêche
    """
    xi,yi,zi = vecI
    xf,yf,zf =  vecI + vecDir*l
    u,v,w = vecDir
    color = 'rgb({},{},{})'.format(rgb[0],rgb[1],rgb[2])

    cone = go.Cone(
    x=[xf], y=[yf], z=[zf],
    u=[u], v=[v], w=[w],
    showscale=False,
    cauto=True,
    sizemode='absolute',
    sizeref=s,
    colorscale=[[0, color], [1, color]],
    anchor='cm'
     )

    tige = go.Scatter3d(
    x =[xi,xf], y=[yi,yf], z=[zi,zf],
    mode='lines',
    line=dict(
        width=5, color=color
    ) )

    return cone,tige


def plotte(surf, ecran, cam1, cam2, L, t, d):

    # codes rgb
    rgb_ecran=()
    rgb_grille_i=()
    rgb_grille_f=()
    rgb_cam1=()
    rgb_cam2=()

    # Vecteurs unitaires
    dirCam1 = cam1.camToEcran(np.array([0,0,1]))
    dirCam2 = cam2.camToEcran(np.array([0,0,1]))
    dirEcran = np.array([0,0,1])
    dirRecherche = d

    # PLANS :
    data_ecran = go.Mesh3d(
        x = [0,ecran.W[0],0,ecran.W[0]],
        y = [0,0,ecran.W[1],ecran.W[1]],
        z = [0,0,0,0],
        color='rgb({},{},{})'.format(rgb_ecran[0],rgb_ecran[1],rgb_ecran[2])
        )
    # Grille initiale
    data_grille_init = go.Mesh3d(
        x = surf.x_i,
        y = surf.y_i,
        z = surf.z_i,
        color='rgb({},{},{})'.format(rgb_grille_i[0],rgb_grille_i[1],rgb_grille_i[2])
        )
    # Grille finale
    data_grille_finale= go.Mesh3d(
        x = surf.x_f,
        y = surf.y_f,
        z = surf.z_f,
        color='rgb({},{},{})'.format(rgb_grille_f[0],rgb_grille_f[1],rgb_grille_f[2])
        )
    data = [data_ecran, data_grille_finale, data_grille_init]
    # FLECHES
    # ecran
    data.append( fleche(vecI, vecDir, rgb=(0,0,0), s=1/10, l=1)  )
    # cam1
    data.append( fleche(vecI, vecDir, rgb=(0,0,0), s=1/10, l=1)  )
    # cam2
    data.append( fleche(vecI, vecDir, rgb=(0,0,0), s=1/10, l=1)  )
    # recherche
    data.append( fleche(vecI, vecDir, rgb=(0,0,0), s=1/10, l=1)  )

    fig = go.Figure(data)
    fig.update_layout(scene = dict(
                    xaxis_title='X',
                    yaxis_title='Y',
                    zaxis_title='Z'))

    # fix the ratio in the top left subplot to be a cube
    fig.update_layout(scene_aspectmode='cube')
    # fig.write_image("fig_{}.eps".format(stra))
    fig.show()


# Visualisation en matplotlib -------------------------------------------------------
def show_plt(surf, cam1, cam2, t, d, L):

    fig=plt.figure()
    ax = Axes3D(fig, azim=-32, elev=1)
    ax.auto_scale_xyz([0, 1], [0, 1], [0, 1])
    set_aspect_3D(cam1, ax)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    ax.scatter( surf.x_f, surf.y_f, surf.z_f, marker='.', color='r')

    dirCam1 = cam1.camToEcran(np.array([0,0,1]))*L
    dirCam2 = cam2.camToEcran(np.array([0,0,1]))*L

    ax.scatter(0,0,0)
    ax.quiver(0,0,0,0,0,-L)

    ax.scatter(cam1.S[0], cam1.S[1], cam1.S[2], marker='x',color='blue')
    ax.quiver(cam1.S[0], cam1.S[1], cam1.S[2], dirCam1[0], dirCam1[1], dirCam1[2])

    ax.scatter(cam2.S[0], cam2.S[1], cam2.S[2], marker='x')
    ax.quiver(cam2.S[0], cam2.S[1], cam2.S[2], dirCam2[0], dirCam2[1], dirCam2[2])

    ax.quiver(t[0],t[1],t[2], d[0]*L, d[1]*L, d[2]*L)

    plt.show()


def set_aspect_3D(cam, ax):
    ## Set aspect -----------------------------------------
    X=np.array([0, cam.S[0]])
    Y=np.array([0, cam.S[1]])
    Z=np.array([0, cam.S[2]])
    # Create cubic bounding box to simulate equal aspect ratio
    max_range = np.array([X.max()-X.min(), Y.max()-Y.min(), Z.max()-Z.min()]).max()
    Xb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][0].flatten() + 0.5*(X.max()+X.min())
    Yb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][1].flatten() + 0.5*(Y.max()+Y.min())
    Zb = 0.5*max_range*np.mgrid[-1:2:2,-1:2:2,-1:2:2][2].flatten() + 0.5*(Z.max()+Z.min())
    # Comment or uncomment following both lines to test the fake bounding box:
    for xb, yb, zb in zip(Xb, Yb, Zb):
       ax.plot([xb], [yb], [zb], 'w')
    ## Set aspect -----------------------------------------


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
