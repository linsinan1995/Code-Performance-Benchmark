#!/bin/bash

cc=g++-8
niter=30

for bm in 100 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400 1500
do
    rm -f $bm.txt

	$cc -std=c++11 -DBLOCK_SIZE=$bm manual-blocking.cpp -O2 -fno-dce -o $bm
    
	for i in $(eval echo "{1..$niter}")
    do
        echo "=====Running benchmark $bm - iter $i=====" 
        nice -n -19 ./$bm $i $i+1 >> $bm.txt
    done
    printf "\n"
done
