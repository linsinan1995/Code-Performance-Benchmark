# create assembler code:
g++ -std=c++11 -S -fverbose-asm -g -O2 nounroll.cpp -o no-unroll.s
# create asm interlaced with source lines:
as -alhnd no-unroll.s > no-unroll.lst

# create assembler code:
g++ -std=c++11 -S -fverbose-asm -g -O2 unroll-prev-7.cpp -o unroll.s
# create asm interlaced with source lines:
as -alhnd unroll.s > unroll.lst
