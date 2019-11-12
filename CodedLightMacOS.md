##### 1. `cmake`
```$ brew install cmake```

##### 2. `OpenCV`
```$ brew install OpenCV```

Then:

```$ echo /usr/local/opt/opencv/lib/python3.7/site-packages >> /usr/local/lib/python3.7/site-packages/opencv.pth ```

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
$ mkdir -p ~/src
$ cd ~/src
$ git clone --recursive https://github.com/openthread/openthread.git
$ cd openthread
$ ./script/bootstrap
$ ./bootstrap
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
$ sudo make install
