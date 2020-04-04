createDir () {
   local $1
   if [ ! -d "$1" ]; then
       mkdir "$1"
   fi
}

main () {

  # sh cleanFolder
  # cd tnm-opencv
  # createDir "data_AV"
  # createDir "data_PG"

  # python calibration.py

  cmake .
  make
  ./callibExt

}

main
