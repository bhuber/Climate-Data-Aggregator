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
	for j in $i
	do
		python ../py/dataimport.py "$i$pre${j:3}" "$i$max${j:3}" "$i$min${j:3}"
	done
done
