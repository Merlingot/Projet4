#!/bin/bash
createDir () {
   local $1
   if [ ! -d "$1" ]; then
       mkdir "$1"
   fi
}

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
