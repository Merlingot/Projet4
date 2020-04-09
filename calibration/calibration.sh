createDir () {
   local $1
   if [ ! -d "$1" ]; then
       mkdir "$1"
   fi
}

main () {

  python calibration.py

  cd build

  cmake ../tnm-opencv
  make
  ./calibexeAV
  ./calibexePG
}

main
