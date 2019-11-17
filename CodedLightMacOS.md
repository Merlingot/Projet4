## Install coded light with homebrew

### 1. `cmake`
```
$ brew install cmake
```

### 2. `OpenCV`
```
$ brew install opencv
```
You have to use OpenCv version 3. Else it does not work. This is how you use the correct version:
```
$ brew search opencv
>>> opencv opencv@2 opencv@3
$ brew install opencv@3
$ brew unlink opencv
$ brew --force link opencv@3
```
Then tell Python where OpenCV is:
```
$ echo /usr/local/opt/opencv/lib/python3.7/site-packages >> /usr/local/lib/python3.7/site-packages/opencv.pth
```
Then:
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
Note1 : Verify `cv2.__version__` in the python version to which it was linked (line 19)

Note2 : `cv2.__version__`is the version that will be used. Should be opencv3. Does not work with opencv4. 

### 3. `Ceres`
```
$ brew install ceres-solver
```

### 4. `xTCLAP`

You need to install TCLAP first:
```
$ brew install tclap
```
Then install the extension:
```
$ git clone https://bitbucket.org/nicolasmartin3d/xtclap
$ cd xtclap
$ mkdir build && cd build && cmake ..
$ make -j4 && make install
```
Note : tutorial does not work for me without xtclap

### 5. `MVG`

Install the OpenThreads library:
```
$ brew install openscenegraph
```
Note: the OpenSceneGraph library contains the OpenThreads library. This is the only I have found possible to install the OpenThread lib.

Install MVG
```
$ brew install wget 
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
Note : git version had an error. bitbucket version is error free. 


## Additional things:

### a. Link `Qt` 
```
$ echo 'export PATH="/usr/local/opt/qt/bin:$PATH"' >> ~/.bash_profile
$ export LDFLAGS="-L/usr/local/opt/qt/lib"
$ export CPPFLAGS="-I/usr/local/opt/qt/include"
$ export PKG_CONFIG_PATH="/usr/local/opt/qt/lib/pkgconfig"
```








