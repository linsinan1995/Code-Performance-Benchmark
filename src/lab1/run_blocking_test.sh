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

for size in 10 50 100 200 300 400 500 600 700 800 900 1000 1100 1200 1300 1400 1500
do
	g++-8 -DBLOCK_SIZE=$size test_block.cpp -O2 -o $size
	printf "g++-8 -DBLOCK_SIZE=$size test_block.cpp -O2 -o $size\n"
	echo "BLOCK_SIZE = $size\n" >> test_block.txt
	nice -n -19 ./$size >> test_block.txt
done
