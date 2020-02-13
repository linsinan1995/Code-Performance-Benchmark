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
from scipy.stats import t, ttest_ind
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


class Visualization:
    def __init__(self, data):
        self.data = data

    
    def benchmark(self, compilers, dir_to_data, save_pic = False, nloop = 10):
        plt.title('{} times matrix computation Benchmark'.format(nloop))

        print(self.data.describe())
        print("\n")
        ax = self.data.boxplot(showmeans=True, figsize=(6,8))
        ax.set_ylabel('Micro-Second')
        ax.set_xlabel('Compiler Names')
        plt.tight_layout()
        if save_pic:
            if not os.path.exists("pics"):
                os.makedirs("pics")
            plt.savefig('pics/result.png', dpi = 200)
        plt.show()
        return self.data.describe().to_html().replace("\n"," ")

    def t_test(self, cplName1, cplName2, alpha = 0.05, save_pic = True):
        
        print("Hypothesis 0: compiler {0} is faster or equal to compiler {1}, \nHypothesis 1: compiler {0} is slower than compiler {1}".format(cplName1, cplName2))
        # print("Hypothesis 0: compiler {0} is >= to compiler {1}, \nHypothesis 1: compiler {0} is < compiler {1}".format(cplName1, cplName2))
        t_value, p = ttest_ind(self.data[cplName1], self.data[cplName2], equal_var=False)

        diff = self.data[cplName1] - self.data[cplName2]
        df = len(self.data)-1 # degree of freedom

        t_alpha_percentile = t.ppf(1 - alpha / 2, df)

        print("P value is {}, t value is {}".format(p/2, t_value))
        if (p/2 < alpha and t_value > 0):
            print("REJECT the null hypothesis\n")
        else:
            print("ACCEPT the null hypothesis\n")

        plt.figure(0)
        rv = t(df)
        limit = np.minimum(rv.dist.b, 5)
        x = np.linspace(-1 * limit, limit)
        h = plt.plot(x, rv.pdf(x), label = 'Student\'s t distribution')
        plt.xlabel('x')
        plt.ylabel('t(x)')
        plt.title('Difference significance test -- {} v.s. {}'.format(cplName1, cplName2))
        plt.grid(True)
        plt.axvline(x = t_alpha_percentile, ymin = 0, ymax = 0.095, 
                linewidth=2, color='r', label = '(1-$\\alpha$ / 2) percentile')
        plt.axvline(x = t_value, ymin = 0, ymax = 0.6, 
                linewidth=2, color='g', label = 't value')

        plt.annotate('(1-$\\alpha$ / 2) percentile', xy = (t_alpha_percentile, 0.05),
                xytext=(t_alpha_percentile + 0.5, 0.09), arrowprops=dict(facecolor = 'black', shrink = 0.05),)
        plt.annotate('t value', xy = (t_value, 0.26),
                xytext=(t_value + 0.5, 0.30), arrowprops=dict(facecolor = 'black', shrink = 0.05),)

        leg = plt.legend()

        frame = leg.get_frame()
        frame.set_facecolor('0.80')
        for i in leg.get_texts():
            i.set_fontsize('small')

        for l in leg.get_lines():
            l.set_linewidth(1.5)

        diff_mean = np.mean(diff)
        diff_std = np.std(diff.values, dtype=np.float64, ddof=1)

        normalized_sample = (diff - diff_mean) / (diff_std / math.sqrt(len(diff)))
        plt.plot(normalized_sample, [0]*len(normalized_sample), 'ro')
        plt.tight_layout()
        if save_pic:
            if not os.path.exists("pics"):
                os.makedirs("pics")
            plt.savefig('pics/{}_{}.png'.format(cplName1, cplName2), dpi = 150)
        plt.close()
        # plt.show()
    



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter times of executing')
    parser.add_argument('-n', '--nloop', type=int, default = 10)
    parser.add_argument('-d', '--debug', action='store_const',
                    const=True, default=False)
    parser.add_argument('-s', '--savepic', action='store_const',
                    const=True, default=False)
    # parser.add_argument('--justPlot', type=bool, default = False)
    parser.add_argument('-jp', '--justPlot', action='store_const',
                    const=True, default=False)

    args = parser.parse_args()
    
    # Config
    mainFile = "main.c"
    compilers = ["javac", "gcc", "clang", "icc"]
    MAX_ROW, MAX_COL = getShape(mainFile)

    dir_to_data = "data"
    if not os.path.exists(dir_to_data):
        os.makedirs(dir_to_data)

    if not args.justPlot:
        for cpl in compilers:
            build = Build(mainFile, args.nloop, cpl, dir_to_data)
            build.run(random.randint(0,MAX_ROW-1), random.randint(0,MAX_COL-1), args.debug)
    
    df = pd.DataFrame(columns=compilers)
    for cpl in compilers:
        path = dir_to_data + "/" + cpl + ".txt"
        data = np.loadtxt(path)
        df[cpl] = data
    
    vis = Visualization(df)
    html = vis.benchmark(compilers, dir_to_data, args.savepic, args.nloop)

    for i in range(len(compilers)):
        for j in range(i+1, len(compilers)):
            vis.t_test(compilers[i], compilers[j], 0.05, args.savepic)
    