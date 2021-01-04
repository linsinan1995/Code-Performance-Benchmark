#!/bin/bash

cc=g++-8 
niter=30
rm -f manual_unroll
$cc -std=c++11 manual-unroll-7.cpp -O2 -o manual_unroll
for i in $(eval echo "{1..$niter}")
do
	echo "=====Running benchmark mamnual unroll - iter $i=====" 
    nice -n -19 ./manual_unroll $i $i+1 >> manual_unroll.txt
done
printf "\n"

$cc -DUNROLL -std=c++11 original.cpp -O2 -funroll-loops -o unroll -fopt-info 
for i in $(eval echo "{1..$niter}")
do
	echo "=====Running benchmark unroll - iter $i=====" 
	nice -n -19 ./unroll $i $i+1 >> unroll.txt
done
printf "\n"

m -f original
$cc -std=c++11 original.cpp -O2 -o original
for i in $(eval echo "{1..$niter}")
do
	
	echo "=====Running benchmark original - iter $i=====" 
	nice -n -19 ./original $i $i+1 >> original.txt
done
printf "\n"
