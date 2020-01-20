## Installer CodedLight sur un mac

### 1. `cmake`
```
$ brew install cmake
```

### 2. `OpenCV`

##### Avec conda:
```
$ conda install opencv
```
Test:
```
$ python
>>> import cv2
>>> print( cv2.__version__ )
3.4.2
>>> exit()
```

##### Avec Homebrew:
```
$ brew install opencv
```
Prendre opencv3:
```
$ brew search opencv
>>> opencv opencv@2 opencv@3
$ brew install opencv@3
$ brew unlink opencv
$ brew --force link opencv@3
```
Link:
```
$ echo /usr/local/opt/opencv/lib/python3.7/site-packages >> /usr/local/lib/python3.7/site-packages/opencv.pth
```
Flags:
```
$ echo 'export PATH="/usr/local/opt/opencv@3/bin:$PATH"' >> ~/.bash_profile
$ export LDFLAGS="-L/usr/local/opt/opencv@3/lib"
$ export CPPFLAGS="-I/usr/local/opt/opencv@3/include"
```
Test:
```
$ python3.7
>>> import cv2
>>> print( cv2.__version__ )
3.4.5
>>> exit()
```

### 3. `Ceres`
```
$ brew install ceres-solver
```

### 4. `xTCLAP`

Installer TCLAP:
```
$ brew install tclap
```
Installer l'extension:
```
$ git clone https://bitbucket.org/nicolasmartin3d/xtclap
$ cd xtclap
$ mkdir build && cd build && cmake ..
$ make -j4 && make install
```
Note: Le tutoriel ne marche pas sans xtclap

### 5. `MVG`

Intaller la librarie OpenSceneGraph qui contient la librairie OpenThreads.
```
$ brew install openscenegraph
```

Installer `wget` si tu l'as pas:
```
$ brew install wget
```
Installer MVG
```
$ wget https://bitbucket.org/nicolasmartin3d/mvg/get/1.0.tar.gz
$ tar zxf 1.0.tar.gz
$ cd nicolasmartin3d-mvg-6321c820e7d8
$ mkdir build && cd build && cmake ..
$ make -j4 && make install
```
### 6. `Coded light`
```
$ wget https://bitbucket.org/nicolasmartin3d/codedlight/get/2.0.tar.gz
$ tar zxf 2.0.tar.gz
$ cd nicolasmartin3d-codedlight-bdd3423492dd
$ mkdir build && cd build && cmake ..
$ make -j4 && make install
```
Note : La version git a un bug dedans.


## Trucs additionels:

### a. Link `Qt`
```
$ echo 'export PATH="/usr/local/opt/qt/bin:$PATH"' >> ~/.bash_profile
$ export LDFLAGS="-L/usr/local/opt/qt/lib"
$ export CPPFLAGS="-I/usr/local/opt/qt/include"
$ export PKG_CONFIG_PATH="/usr/local/opt/qt/lib/pkgconfig"
```
