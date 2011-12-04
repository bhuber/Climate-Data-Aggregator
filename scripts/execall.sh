#! /bin/bash

#Usage: execall.sh '/path/to/PRCP/' '/path/to/MAX Temp/' '/path/to/MIN TEMP/'
#Don't forget the trailing slashes!

A="$1"
B="$2"
C="$3"

d=`ls $A`

pres="pre"
maxs="tmax"
mins="tmin"


for i in $d
do
	#echo $i
	for j in `ls $A$i` 
	do
		#echo $j
		suffix=${j:(-12)}
		#echo $suffix
		python ../py/dataimport.py "$A$i/$pres.$suffix" "$A$i/$maxs.$suffix" "$A$i/$mins.$suffix"
	done
done
