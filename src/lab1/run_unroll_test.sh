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

for size in 1 2 3 
do
	printf "g++-8 -DUNROLL_TYPE=$size test_unroll.cpp -O2 -o $size\n"
	g++-8 -DUNROLL_TYPE=$size test_unroll.cpp -O2 -o $size -fopt-info
	echo "UNROLL TYPE = $size\n" >> test_unroll.txt
	nice -n -19 ./$size >> test_unroll.txt
done
