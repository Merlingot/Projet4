#!/bin/bash


cleanDir () {
   local $1
   if [ -d "$1" ]; then
     if [ ! -z "$(ls -A $1)" ]; then
       rm -r "$1"/*
     fi
   fi
}

removeDir () {
   local $1
   if [ -d "$1" ]; then
       rm -r "$1"
   fi
}

cleanFile () {
  local $1
  if [ -f "$1" ]; then
      rm "$1"
  fi
}

main () {

pwd

echo "Clean directory (y/n)? "
read answer
if [ "$answer" != "${answer#[Yy]}" ] ;then
    echo Yes
    cleanDir "build"
    cleanDir "data_AV"
    cleanDir "data_PG"
else
    echo No
fi
}

main
