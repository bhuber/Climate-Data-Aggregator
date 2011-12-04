#! /bin/bash

#Usage: execall.sh '/path/to/test/data/'
#Don't forget the trailing slashes!

python ../py/dataimport.py "${1}pre.20061231.asc"  "${1}tmax.20061231.asc" "${1}tmin.20061231.asc"

