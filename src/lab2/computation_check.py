import itertools
import numpy as np
import re

def getShape(file):
    with open(file, "r") as f:
        content = f.readlines()
        for line in content:
            if "#define N" in line:
                N = int(re.sub("\D", "", line))
            if "#define M" in line:
                M = int(re.sub("\D", "", line))
            if "#define P" in line:
                P = int(re.sub("\D", "", line))
    return N,M,P

#########################GENERATE RANDOM MATRIX#####################################
N, M, P = getShape("interchange.cpp")

if 0: # we just need to generate once
    A = np.random.rand(N, P)
    B = np.random.rand(P, M)
    C = A.dot(B)

    np.savetxt("test/A.txt", A)
    np.savetxt("test/B.txt", B)
    np.savetxt("test/C.txt", C)

data_path = ["test/C_%s.txt" % (i+j+z) for i,j,z in itertools.permutations("NMP", 3)]

C = np.loadtxt("test/C.txt")

for path in data_path:
    C_test = np.loadtxt(path)
    print(path + ": %f" % np.abs(C-C_test).sum())