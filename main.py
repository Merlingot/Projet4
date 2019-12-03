import matplotlib.pyplot as plt
import numpy as np
import cv2
from skimage.io import imread, imsave
import seaborn as sns

from Camera import Camera
from Ecran import Ecran

# Setup
w = np.array( [1600, 900] )
W = w * 0.277e-3
c = np.array( [800, 450] )
ecran = Ecran( W, w, c)

# Parametre de calibration provenant de l'annee derniere

K = np.array([[10346.85, 0., 0.],
             [0., 10347.03, 0.],
             [1611.22, 1363.49, 1.]])

R = np.array([[-0.998, 0.01193, 0.01183],
             [-0.003297, 0.7564, -0.6541],
             [-0.02205, -0.6540, -0.7262]])

T = np.array([56.368, -156.815, 142.289])

w = np.array( [3376, 2704] )
W = w * 1.69e-6

sgmf = "cam_match.png"

cam = Camera(ecran, K, R, T, W, w, sgmf)


