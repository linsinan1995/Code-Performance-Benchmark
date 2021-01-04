#!/bin/bash

cc=g++-8
niter=30

for bm in "MNP" "MPN" "NMP" "NPM" "PMN" "PNM"
do
    rm -f $bm.txt
    printf "======Compiling benchmark -- $bm======\n"

	$cc -std=c++11 -D$bm manual-interchange.cpp -O2 -fno-dce -o $bm
    
	for i in $(eval echo "{1..$niter}")
    do
        echo "=====Running benchmark $bm - iter $i=====" 
        nice -n -19 ./$bm $i $i+1 >> $bm.txt
    done
    printf "\n"
done
rm -f original.txt

g++-8 -std=c++11 -DORIGINAL manual-interchange.cpp -O2 -floop-interchange -fno-dce -o original
for i in $(eval echo "{1..$niter}")
do 
	echo "====-floop-interchange - iter $i====="
	nice -n -19 ./original $i $i+1 >> original.txt
done
