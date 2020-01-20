import numpy as np

def sauce(v1,v2,v3,t, hx, hy, kx, ky):
    u1 = v1
    e1 = u1/np.linalg.norm(u1)
    u2 = v2 - np.dot(u1, v2)*e1
    e2 = u2/np.linalg.norm(u2)
    u3 = v3 - np.dot(u1, v3)*e1 - np.dot(u2, v3)*e2
    e3 = u3/np.linalg.norm(u3)

    grille = []
    o = t/2
    for i in np.arange(-kx, kx):
        for j in np.arange(-ky, ky):
            a = o + i*hx*e2 + j*hy*e3
            grille.append(a)
    return grille


R1 = np.array([[-0.998, 0.01193, 0.01183],
             [-0.003297, 0.7564, -0.6541],
             [-0.02205, -0.6540, -0.7262]])

T1 = np.array([56.368, -156.815, 142.289])



e = np.array([0,0,1])
c = R1@e
v1 = -(e + c)
#
v2 = np.cross(e,v1)
v3 = np.cross(v2,v1)


grille = sauce(v1, v2, v3, T1, 1, 1, 10, 10)
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
fig=plt.figure()
ax=fig.add_subplot(111, projection='3d')

plt.figure()
for i in grille:
    ax.scatter( i[0], i[1], i[2])
ax.scatter(e[0], e[1], e[2])
ax.scatter(T1[0], T1[1], T1[2])
plt.show()
