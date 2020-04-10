main () {

  python calibration.py

  cd build

  cmake ../tnm-opencv
  make
  ./calibexeAV
  ./calibexePG
}

main
