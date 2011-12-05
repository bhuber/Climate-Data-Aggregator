#!/bin/bash

#Usage: importByYear.sh /path/to/unzipped/data/
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
	#append ${pres}* so we only list one set of variable files, otherwise we import everything x3
	for j in `ls $A$i/${pres}*` 
	do
		#echo $j
		suffix=${j:(-12)}
		#echo $suffix
		cmd="python ../py/dataimport.py"
		#cmd="echo"
		$cmd "$A$i/$pres.$suffix" "$A$i/$maxs.$suffix" "$A$i/$mins.$suffix"
	done
done

