import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import cv2
from skimage.io import imread, imsave
import seaborn as sns


img = cv2.imread("test/AV/img0000.png")

cv2.imshow("allo",img)

cv2.waitKey(0)




# ####################################################################################
# ## - Donnnees

# R1 = np.array([[-0.998, 0.01193, 0.01183],
#              [-0.003297, 0.7564, -0.6541],
#              [-0.02205, -0.6540, -0.7262]])


# T1 = np.array([56.368, -156.815, 142.289])

# ##################################################################################
# ## - calcul vecteurs camera

# ex = np.array([1,0,0])
# ey = np.array([0,1,0])
# ez = np.array([0,0,1])

# cx = np.dot( R1, ex )
# cx /= np.linalg.norm(cx)
# cy = np.dot( R1, ey )
# cy /= np.linalg.norm(cy)
# cz = -np.cross(cx,cy)
# cz /= np.linalg.norm(cz)
# #c = -np.dot(R1, e )


# #########################################################################################3

# v1 = -(-ez + cz)

# #v2 = np.cross(ez,v1)
# #v3 = np.cross(v2,v1)

# v2 = ex
# v3 = ey

# V = np.concatenate((v1,v2,v3), axis=0).reshape(3,3)
# print(np.linalg.det(V))
# #grille = sauce(v1, v2, v3, T1, 1, 1, 10, 10)

# u1 = v1
# e1 = u1/np.linalg.norm(u1)
# u2 = v2 - ( np.dot(u1, v2) / np.dot(u1,u1) ) * u1
# e2 = u2/np.linalg.norm(u2)
# u3 = v3 - ( np.dot(u1, v3) / np.dot(u1,u1) ) * u1 - ( np.dot(u2, v3) / np.dot(u2,u2) ) * u2
# e3 = u3/np.linalg.norm(u3)

# fig=plt.figure()
# ax=fig.add_subplot(111, projection='3d')

# ## - Plan
# grille = []
# k=10
# hx=1
# hy=1
# o = T1/2
# for i in np.arange(-k, k):
#     for j in np.arange(-k, k):
#         a = o + i*hx*e2 + j*hy*e3        # - 100*e1
#         grille.append(a)

# for i in grille:
#     ax.scatter( i[0], i[1], i[2])

# X = T1/2
# Y = 20*e1
# ax.quiver(X[0], X[1], X[2], Y[0], Y[1], Y[2])
# Y = 20*e2
# ax.quiver(X[0],X[1], X[2], Y[0], Y[1], Y[2])
# Y = 20*e3
# ax.quiver(X[0],X[1], X[2], Y[0], Y[1], Y[2])

# ## - Camera
# grille = []
# o = T1
# k = 10
# for i in np.arange(0, k):
#     for j in np.arange(0, k):
#         a = o + i*cx + j*cy
#         grille.append(a)

# for i in grille:
#     ax.scatter( i[0], i[1], i[2])

# cx*=20
# cy*=20
# cz*=20
# ax.quiver(T1[0], T1[1], T1[2], cx[0], cx[1], cx[2])
# ax.quiver(T1[0], T1[1], T1[2], cy[0], cy[1], cy[2])
# ax.quiver(T1[0], T1[1], T1[2], cz[0], cz[1], cz[2])

# ## - Ecran
# grille = []
# o = [0,0,0]
# k = 10
# for i in np.arange(0, k):
#     for j in np.arange(0, k):
#         a = o + i*ex + j*ey
#         grille.append(a)

# for i in grille:
#     ax.scatter( i[0], i[1], i[2])

# ez *= 20
# ax.quiver(0, 0, 0, ez[0], ez[1], ez[2])


# ax.set_xlim([-100,100])
# ax.set_ylim([-180,20])
# ax.set_zlim([0,200])

# plt.show()
