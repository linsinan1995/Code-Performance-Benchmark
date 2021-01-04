import argparse
import numpy as np
import re

N, M, P = 2100, 1600, 2000

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-test', action='store_true', help='test the output of exec file')
    args = parser.parse_args()

    is_test = args.test

    if not is_test:
        A = np.random.rand(N, P).astype(np.float32)
        B = np.random.rand(P, M).astype(np.float32)

        np.savetxt("A.txt", A, fmt='%.5f')
        np.savetxt("B.txt", B, fmt='%.5f')
    else:
        a = np.loadtxt("A.txt").astype(np.float32)
        b = np.loadtxt("B.txt").astype(np.float32)
        c = np.around(a.dot(b), decimals=5)
        c_out = np.loadtxt("C_out.txt")
        dev = np.abs(c-c_out).sum()
        print("average absolute error: ", dev/(c_out.shape[0]*c_out.shape[1]))
        print("average deviation rate: {:.4f}%".format(100*dev/np.abs(c).sum()))