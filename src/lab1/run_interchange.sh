#!/bin/sh

#================================================================
#   Copyright (C) 2020 Sangfor Ltd. All rights reserved.
#   
#   Filename   ：run_blocking_test.sh
#   Author     ：Lin Sinan
#   Date       ：2020-06-19
#   Description：
#
#================================================================

for size in None MNP MPN NMP NPM PNM PMN 
do
	printf "g++-8 -D$size test_interchange.cpp -O2 -o interchange\n"
	g++-8 -D$size test_interchange.cpp -O2 -o interchange -fopt-info
	echo "TYPE = $size\n" >> test_interchange.txt
	nice -n -19 ./interchange >> test_interchange.txt
done
