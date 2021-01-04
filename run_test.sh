#!/bin/bash
FILES=test/bin/*

cc=g++-8
file=original.cpp
option=

rm -f C_out.* A.txt B.txt C.txt

# generate input matrix
python check_accuracy.py
for file in $FILES
do
  echo "Testing $file execute file..."
  ./$file 1 1 > C_out.txt
  # compare computing result through numpy
  python check_accuracy.py -test
done

rm -f C_out.* A.txt B.txt C.txt
