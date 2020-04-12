
# import csv
# data = zip(surf.x_f, surf.y_f, surf.z_f)
#
# with open("miroir.csv", "a") as f:
#     coords = [map(str, tupl) for tupl in data]
#     writer = csv.writer(f, delimiter=',')
#
#     for line in coords:
#         writer.writerow(line)


import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


def f(z, a,b,c):
    return a + np.exp(b*z) + np.exp(-c*z)

final_points=[]
for p in surf.good_points:
    z = p.vecP[:,2]; v=p.vecV
    if len(z)>3:
        try:
            signal = sci.savgol_filter(v, int(len(p.vecV)/2)*2 - 1 , 4)
            # popt,pcov = curve_fit(f,z,signal)
            # fit = f(z,*popt)
            index = sci.argrelextrema( signal, np.less)[0]
            # if len(index)==1:
            #     final_points.append(p)
            #     p.pfinal=p.vecP[index[0]]
            #     p.vfinal= p.vecV[index[0]]
            if len(index)==1:
                plt.figure()
                fig, ax2 = plt.subplots(1,1)
                ax2.plot(z, v, '.')
                ax2.plot(z, signal)
                # ax2.plot(z, fit, '--')
                ax2.plot(z[index], signal[index], 'o')
                plt.show()
        except RuntimeError:
            pass
        except ValueError:
            pass



# Find plane
xs = np.genfromtxt('data.csv', usecols=(0), delimiter=',')
ys = np.genfromtxt('data.csv', usecols=(1), delimiter=',')
zs = np.genfromtxt('data.csv', usecols=(2), delimiter=',')


# plot raw data
plt.figure()
ax = plt.subplot(111, projection='3d')
ax.scatter(xs, ys, zs, color='b')


# do fit
tmp_A = []
tmp_b = []
for i in range(len(xs)):
    tmp_A.append([xs[i], ys[i], 1])
    tmp_b.append(zs[i])
b = np.matrix(tmp_b).T
A = np.matrix(tmp_A)
fit = (A.T * A).I * A.T * b
errors = b - A * fit
residual = np.linalg.norm(errors)

print ("solution:")
print ("%f x + %f y + %f = z" % (fit[0], fit[1], fit[2]))
print ("errors:")
print (errors)
print ("residual:")
print (residual)
fit.item(0)
fit

X,Y = np.meshgrid(xs, ys)
# plot plane
plt.figure()
ax = plt.subplot(111, projection='3d')
ax.scatter(xs, ys, zs, color='b')
Z = fit.item(0) * X + fit.item(1) * Y + fit.item(2)
ax.plot_wireframe(X,Y,Z, color='k')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()

n=np.array([-fit.item(0), fit.item(1), 1])
n=n/np.linalg.norm(n)
a=np.array([0,0,1])
v=np.cross(a, n)
s=np.linalg.norm(v)
c=a@n
matv = np.array([ [0,-v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0] ])
R = np.eye(3) + matv + matv@matv*(1-c)/(s**2)

a,b,c,d,e,f,g,h,i = R.ravel()
xcac = a*zs+ b*ys + c*zs
ycac = d*zs + e*ys + f*zs
zcac = g*zs + h*ys + i*zs

# plot plane
plt.figure()
ax = plt.subplot(111, projection='3d')
ax.scatter(xcac, ycac, zcac, color='b')
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')
plt.show()
