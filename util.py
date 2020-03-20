import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objects as go
import numpy as np



def plotte(surf, ecran, cam1, cam2, L):
    fig = go.Figure()

    # Écran (0,0) (Wx,0) (0,Wy) (Wx, Wy)
    data_ecran = go.Surface(
        x = [0,ecran.Wx,0,ecran.Wx],
        y = [0,0,ecran.Wy,ecran.Wy],
        z = [0,0,0,0],
        color='cyan'
        )
    # Grille initiale
    data_grille_init = go.Surface(
        x = surf.x_i,
        y = surf.y_i,
        z = surf.z_i,
        color='pink'
        )
    # Grille finale
    data_grille_finale= go.Surface(
        x = surf.x_f,
        y = surf.y_f,
        z = surf.z_f,
        color='magenta'
        )

    fig.update_layout(scene = dict(
                    xaxis_title='X',
                    yaxis_title='Y',
                    zaxis_title='Z'))

    # fix the ratio in the top left subplot to be a cube
    fig.update_layout(scene_aspectmode='cube')
    fig.show()





# Visualisation -------------------------------------------------------
def show_plt(surf, cam1, cam2, t, d):

    fig=plt.figure()
    ax = Axes3D(fig, azim=-32, elev=1)
    ax.auto_scale_xyz([0, 1], [0, 1], [0, 1])
    set_aspect_3D(cam1, ax)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    ax.scatter( surf.x_f, surf.y_f, surf.z_f, marker='.', color='r')

    L=100e-2 #Longueur flêches
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
