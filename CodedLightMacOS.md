## Install coded light with homebrew

##### 1. `cmake`
```$ brew install cmake```

##### 2. `OpenCV`
```
$ brew install opencv
$ brew search opencv
>>> opencv opencv@2 opencv@3
$ brew install opencv@3
$ brew unlink opencv
$ brew --force link opencv@3
```
Then:

```
$ echo /usr/local/opt/opencv/lib/python3.7/site-packages >> /usr/local/lib/python3.7/site-packages/opencv.pth
$ echo 'export PATH="/usr/local/opt/opencv@3/bin:$PATH"' >> ~/.bash_profile 
$ export LDFLAGS="-L/usr/local/opt/opencv@3/lib"
$ export CPPFLAGS="-I/usr/local/opt/opencv@3/include"
```

Test:

```
$ python3.7
>>> import cv2
>>> print( cv2.__version__ ) 
4.1.2
>>> exit()
```

##### 3. `Ceres`
```$ brew install ceres-solver```

##### 4.MVG

Install OpenThreads

```
$ brew install openscenegraph
```
Install MVG

```
$ brew install wget 
$ wget https://bitbucket.org/nicolasmartin3d/mvg/get/1.0.tar.gz
$ tar zxf 1.0.tar.gz
$ cd nicolasmartin3d-mvg-6321c820e7d8
$ mkdir build && cd build 
$ cmake ..
$ make -j4
$ make install
```
##### 4.Coded light

```
$ wget https://bitbucket.org/nicolasmartin3d/codedlight/get/2.0.tar.gz
$ tar zxf 2.0.tar.gz
$ cd nicolasmartin3d-codedlight-bdd3423492dd
$ mkdir build 
$ cd build
$ cmake ..
$ make -j4
$ make install
```
##### Link Qt
```
$ echo 'export PATH="/usr/local/opt/qt/bin:$PATH"' > ~/.bash_profile
$ export LDFLAGS="-L/usr/local/opt/qt/lib"
$ export CPPFLAGS="-I/usr/local/opt/qt/include"
$ export PKG_CONFIG_PATH="/usr/local/opt/qt/lib/pkgconfig"
```








