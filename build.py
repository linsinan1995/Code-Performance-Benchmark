'''
@Author: Lin Sinan
@Github: https://github.com/linsinan1995
@Email: mynameisxiaou@gmail.com
@LastEditors  : Lin Sinan
@Description: 
              
              
              
'''
import sys,os
import re
import argparse
import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import  t
import math

class Build(object):
    def __init__(self, filename, nTimes, compiler, output):
        self.nTimes = nTimes
        self.compiler = compiler
        self.output = output + "/" + compiler + ".txt"
        if compiler != "javac":
            os.system("{0} -O3 -o execute_{0} {1}".format(compiler, filename))
            if not os.path.exists("build"):
                os.makedirs("build")
            # print("mv execute_{0} build/execute_{0}".format(compiler))
            os.system("mv execute_{0} build/execute_{0}".format(compiler))
        else:
            os.system("javac Matrix.java")
            
    def run(self, nCol, nRow, debug = False):
        os.system("rm {}".format(self.output))
        for i in range(self.nTimes):
            if debug:
                if self.compiler != "javac":
                    os.system("./build/execute_{} {} {}  >> {}"
                        .format(self.compiler, nCol, nRow, self.output))
                else:
                    os.system("java Matrix >> {}".format(self.output))
            else:
                if self.compiler != "javac":
                    os.system("./build/execute_{} {} {} | grep -A 1 Timer | grep ^[0-9] >> {}"
                        .format(self.compiler, nCol, nRow, self.output))
                else:
                    os.system("java Matrix {} {} | grep -A 1 Timer | grep ^[0-9] >> {}"
                        .format(nCol, nRow, self.output))

def getShape(file):
    with open(file, "r") as f:
        content = f.readlines()
        for line in content:
            if "#define N" in line:
                row = int(re.sub("\D", "", line))
            if "#define M" in line:
                col = int(re.sub("\D", "", line))
    return row, col
    
def vis(compilers, dir_to_data, save_pic = False, nloop = 10):
    datas = []
    df = pd.DataFrame(columns=compilers)
    for cpl in compilers:
        path = dir_to_data + "/" + cpl + ".txt"
        data = np.loadtxt(path)
        datas.append(data)
        df[cpl] = data

    plt.title('{} times matrix computation Benchmark'.format(nloop))
    print(df.describe())
    ax = df.boxplot(showmeans=True)
    ax.set_ylabel('Micro-Second')
    ax.set_xlabel('Compiler Names')
    if save_pic:
        if not os.path.exists("pics"):
            os.makedirs("pics")
        plt.savefig('pics/result.png')
    plt.show()

def tTest(sample):
    sample_mean = np.mean(sample)
    sample_std = np.std(sample, dtype=np.float64, ddof=1)
    abs_t = math.fabs( sample_mean / (sample_std / math.sqrt(sample_len)) )
    t_alpha_percentile = t.ppf(1 - alpha / 2, df)
    


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter times of executing')
    parser.add_argument('-n', '--nloop', type=int, default = 10)
    parser.add_argument('-d', '--debug', action='store_const',
                    const=True, default=False)
    parser.add_argument('-s', '--savepic', action='store_const',
                    const=True, default=False)
    # parser.add_argument('--justPlot', type=bool, default = False)
    parser.add_argument('-j', '--justPlot', action='store_const',
                    const=True, default=False)
    args = parser.parse_args()
    
    # Config
    mainFile = "main.c"
    compilers = ["icc", "gcc", "clang", "javac"]
    MAX_ROW, MAX_COL = getShape(mainFile)

    dir_to_data = "data"
    if not os.path.exists(dir_to_data):
        os.makedirs(dir_to_data)

    if not args.justPlot:
        for cpl in compilers:
            build = Build(mainFile, args.nloop, cpl, dir_to_data)
            build.run(random.randint(0,MAX_ROW-1), random.randint(0,MAX_COL-1), args.debug)
    
    vis(compilers, dir_to_data, args.savepic, args.nloop)