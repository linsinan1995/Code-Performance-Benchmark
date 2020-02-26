#!/usr/bin/python


'''
@Author: Lin Sinan
@Github: https://github.com/linsinan1995
@Email: mynameisxiaou@gmail.com
@LastEditors: Lin Sinan
@Description: 
              
gcc -xc++ -lstdc++ -shared-libgcc -O3 -std=c++17 main.cpp
gcc -xc++ -lstdc++ -std=c++17 -O3 main.cpp       
clang -std=c++17

gcc -O3 main.c           
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
import json
import subprocess as sp

class Build(object):
    def __init__(self, filename, nTimes, compiler, output_dir, parameter, output, debug = False):
        self.nTimes = nTimes
        self.compiler = compiler
        self.output_path = output_dir +"/"+ output + ".txt"
        self.output = output
        self.debug = debug

        if compiler != "javac":
            if os.path.exists("build/execute_{0}".format(output)):
                self.__compile("rm build/execute_{0}".format(output))
            if self.debug:
                print("{} {} -o execute_{} {}".format(compiler, parameter, output, filename))
            self.__compile("{} {} -o execute_{} {}".format(compiler, parameter, output, filename))
            self.__compile("mv execute_{0} build/execute_{0}".format(output))
        else:
            if debug:
                 print("javac Matrix.java ")
            if os.path.exists("Matrix.class"):
                self.__compile("rm Matrix.class")
            self.__compile("javac Matrix.java ")
            
    def run(self, MAX_ROW, MAX_COL):
        if os.path.exists(self.output_path):
            self.__compile("rm {}".format(self.output_path))
        
        for i in range(self.nTimes):
            nCol, nRow = random.randint(0,MAX_ROW-1), random.randint(0,MAX_COL-1)
            if self.compiler != "javac":
                if self.debug: 
                    print("./build/execute_{} {} {}  >> {}" .format(self.output, nCol, nRow, self.output_path))
                self.__compile("./build/execute_{} {} {} | grep -A 1 Timer | grep ^[0-9] >> {}"
                        .format(self.output, nCol, nRow, self.output_path))
            else:
                self.__compile("java Matrix {} {} | grep -A 1 Timer | grep ^[0-9] >> {}" .format(nCol, nRow, self.output_path))
    def __compile(self, commond):
        sp.call(commond, shell=True)        


def getShape(file):
    with open(file, "r") as f:
        content = f.readlines()
        for line in content:
            if "#define N" in line:
                row = int(re.sub("\D", "", line))
            if "#define M" in line:
                col = int(re.sub("\D", "", line))
    return row, col

def roundInt(_max):
    max_int = int(_max)
    nDigits = len(str(max_int))
    ylim_max = round(max_int/10**(nDigits-1)+0.5, 0) * 10 ** (nDigits-1)
    return ylim_max

class Visualization:
    def __init__(self, data, dir_to_pics):
        self.data = data
        self.dir_to_pics = dir_to_pics

    def benchmark(self, compilers , save_pic = False):
        plt.title('{} times matrix computation Benchmark'.format(len(self.data)))

        print(self.data.describe())
        print("\n")
        ax = self.data.boxplot(showmeans=True, figsize=(6,8))
        ax.set_ylabel('Micro-Second')
        ax.set_xlabel('Compiler Names')
        
        _, _max = plt.ylim()
        plt.ylim(0, _max)
        # plt.ylim(0,roundInt(self.data.max().max()))
        # plt.yticks(np.linspace(*(plt.ylim()),5))
        plt.tight_layout()
        if save_pic:
            if not os.path.exists(self.dir_to_pics):
                os.makedirs(self.dir_to_pics)
            plt.savefig(self.dir_to_pics + '/result.png', dpi = 200)
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
            if not os.path.exists(self.dir_to_pics):
                os.makedirs(self.dir_to_pics)
            plt.savefig('{}/{}_{}.png'.format(self.dir_to_pics, cplName1, cplName2), dpi = 150)
        plt.close()
        # plt.show()
    



if __name__ == "__main__":
    if not os.path.exists("build"):
            os.makedirs("build")
    
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists("pic"):
        os.makedirs("pic")
        
    # Config
    with open('config.json') as json_file:
        config = json.load(json_file)

    cpp_file = "main.cpp"
    nloop, compilers, const_config, cpp_configs, output_names, dir_to_data, dir_to_pics, only_plot, debug = config.values()
    MAX_ROW, MAX_COL = getShape(cpp_file)
    
    if not os.path.exists(dir_to_data):
        os.makedirs(dir_to_data)

    if not only_plot:
        cnt = 0
        for cpl in compilers:
            output = output_names[cnt]
            _config = const_config + " " + cpp_configs[cnt]
            build = Build(cpp_file, nloop, cpl, dir_to_data, _config, output, debug)
            build.run(MAX_ROW, MAX_COL)
            cnt += 1

    if not debug:
        df = pd.DataFrame(columns=output_names)
        for name in output_names:
            print(name)
            path = dir_to_data + "/" + name + ".txt"
            data = np.loadtxt(path)
            df[name] = data
        
        vis = Visualization(df, dir_to_pics)
        html = vis.benchmark(output_names, True)

        for i in range(len(output_names)):
            for j in range(i+1, len(output_names)):
                vis.t_test(output_names[i], output_names[j], 0.05, True)
        