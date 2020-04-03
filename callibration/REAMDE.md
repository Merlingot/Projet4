# Guide du code de callibration avec `OpenCV` et `Takahashi`

### Required Package:
- gcc 
- CMake 3.9 or higher
- Python 2.7 or later and Numpy 1.5 or later
- OpenCV

####  Install `OpenCV`

Installer OpenCV avec CMake. 

Suivre les instructions à :
https://docs.opencv.org/master/df/d65/tutorial_table_of_content_introduction.html

#### Télécharger l'algorithme de Takahashi pour OpenCV 

1. Créer un répertoire pour la callibration
``` 
$ mkdir <tnm-opencv>
$ cd <tnm-opencv>
```
2. Télécharger les fichiers à : https://github.com/computer-vision/takahashi2012cvpr/tree/master/opencv __dans le répertoire <tnm-opencv>__

#### Créer un fichier Cmake 
```
$ cd <tnm-opencv>
$ touch CMakeList.txt
```
  Contenu du fichier:
```
cmake_minimum_required(VERSION 2.8)
project( ProjectName )
find_package( OpenCV REQUIRED )
add_executable( ProjectName  demo.cc )
target_link_libraries( ProjectName  ${OpenCV_LIBS} )
```
  `ProjectName` représente le nom donné à l'exécutable en sortie 

#### Créer et écrire un fichier de callibration qui suit les instructions de Takahashi. Voici un exemple. 
```
$ cd <tnm-opencv>
$ touch <calib>.py
```
Voici un exemple:
```
import cv2
import numpy as np
import os
import glob

# INPUTS ----------------------------------------------------------------------
# Path vers les images de la callibration
PATH='/projet4/Calibration_03_13_2020/ext_manta/*.png'
# Nombre de coins internes au damier
NB_CORNER_WIDTH=5
NB_CORNER_HEIGHT=4
# Largeur d'un carré du damier 
nb_pix = 48 # Largeur d'un carré en pixel
l_pix = 0.277e-3 # Largeur d'un pixel
pix = nb_pix*l_pix
# -----------------------------------------------------------------------------

def calibration(PATH, NB_CORNER_WIDTH, NB_CORNER_HEIGHT, pix):
    # Defining the dimensions of checkerboard
    CHECKERBOARD = (NB_CORNER_WIDTH, NB_CORNER_HEIGHT) #(LARGEUR,HAUTEUR)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    # Creating vector to store vectors of 3D points for each checkerboard image
    objpoints = []
    # Creating vector to store vectors of 2D points for each checkerboard image
    imgpoints = []

    # Defining the world coordinates for 3D points (corners of checkboard)
    objp = np.zeros((1, CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
    objp[0,:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)*pix
    prev_img_shape = None

    # Extracting path of individual image stored in a given directory
    images = glob.glob(PATH)
    n = len(images)
    if n < 1 : 
      print('No images found')
      pass
    else :
      for fname in images:
          img = cv2.imread(fname)
          gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
          # Find the chess board corners
          ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD)
          # If desired number of corners are found in the image then ret = true
          if ret == True:
              objpoints.append(objp)
              # refining pixel coordinates for given 2d points.
              corners2 = cv2.cornerSubPix(gray, corners, (11,11),(-1,-1), criteria)
              imgpoints.append(corners2)

      return objpoints, imgpoints, n

objpoints, imgpoints, n = takahashi(PATH, NB_CORNER_WIDTH, NB_CORNER_HEIGHT, pix)

objpoint = objpoints[0]
m=open("./data/model.txt","w+")
index = [0, NB_CORNER_WIDTH-1, -NB_CORNER_WIDTH]
for j in index :
    c = objpoint[0,j]
    m.write("{} {} {}\n".format(c[0]*pix, c[1]*pix, c[2]*pix))
m.close()

for i in range(n):
    imgpoint = imgpoints[i]
    f=open("./data/input{}.txt".format(i+1),"w+")
    for j in index :
        c = imgpoint[j]
        f.write("{} {}\n".format(c[0,0], c[0,1]))
    f.close()
```

#### Créer un répertoire pour les données à analyser avec l'algorithme de Takahashi
```
$ cd <tnm-opencv>
$ mkdir data 
```

#### Compiler avec CMake
```
$ cd <tnm-opencv>
$ python <calibration.py>
$ cmake .
$ make 
$ ./<ProjectName>
```




----
##### Références : 

- Documentation pour compiler des codes OpenCV avec gcc et CMake:

  https://docs.opencv.org/master/db/df5/tutorial_linux_gcc_cmake.html

- Documentation complète de OpenCV: 

  https://docs.opencv.org/master/

- Tutoriels sur OpenCv : 

  https://docs.opencv.org/master/d6/d00/tutorial_py_root.html
    
- Tutoriels sur la callibration avec OpenCV : 

  1. https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_calib3d/py_calibration/py_calibration.html
  
  2. https://www.learnopencv.com/camera-calibration-using-opencv/
  
- Documentation sur l'algorithme de Takahashi avec OpenCV:

  https://computer-vision.github.io/takahashi2012cvpr/v1/
  
  
