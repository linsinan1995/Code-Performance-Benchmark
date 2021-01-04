import numpy as np
import glob


files=glob.glob("*.txt")

for filename in files:
    print(filename)
    with open(filename) as f:
        it = (line for i, line in enumerate(f) if (i+1) % 3 == 0)
        res = np.genfromtxt(it) 
        np.savetxt(filename.split(".")[0] + "_txt", res)
        print("avg:{:.2f}".format(res.mean()))
        print("min:{:.2f}".format(res.min()))
        print("max:{:.2f}".format(res.max()))
        print("std:{:.2f}".format(res.std()))
        print()
 
