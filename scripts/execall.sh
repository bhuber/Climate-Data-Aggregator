#! /bin/bash

#Usage: execall.sh '/path/to/PRCP/' '/path/to/MAX Temp/' '/path/to/MIN TEMP/'
#Don't forget the trailing slashes!

A="$1"
B="$2"
C="$3"

d=`ls $A`

pres="pre"
maxs="max"
mins="min"


for i in $d
do
	python ../py/dataimport.py "$A$pres${i:3}" "$B$maxs${i:3}" "$C$mins${i:3}"
done
