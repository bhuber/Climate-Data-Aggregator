#!/bin/bash

#Usage: execall.sh '/path/to/PRCP/' '/path/to/MAX Temp/' '/path/to/MIN TEMP/' startYear endYear
#p="/foo/path/to/data"
#./unzip.sh "${p}PRCP/" "${p}MAX TEMP/" "${p}MIN TEMP/" 2000 2006
#Don't forget the trailing slashes!

start="$4"
end="$5"
outputdir="../data/real"

#can't get this working for optional 6th argument, just change outputdir manually
#if [ -n $6 ]; then
	#outputdir="$6"
	#echo $outputdir
#fi
	
pres="prcp"
maxs="tmax"
mins="tmin"

for i in $(seq $start $end)
do
	tar -xzvf "${1}$pres.$i.asc20091104.tar.gz"
	tar -xzvf "${2}$maxs.$i.asc20091016.tar.gz"
	tar -xzvf "${3}$mins.$i.asc20091016.tar.gz"
	#echo "${1}$pres.$i.asc20091016.tar.gz"
	#echo "${2}$mins.$i.asc20091016.tar.gz"
	#echo "${3}$maxs.$i.asc20091104.tar.gz"
	mv $i "$outputdir/$i"
done

