'''
@Author: Lin Sinan
@Github: https://github.com/linsinan1995
@Email: mynameisxiaou@gmail.com
@LastEditors: Lin Sinan
@Description: 
                
'''
import sys,os
import re
import argparse
import random
import numpy as np
import math
import json
import subprocess as sp

class Build(object):
    def __init__(self, filename, nTimes, compiler, parameter, output, debug = False):
        self.nTimes = nTimes
        self.compiler = compiler
        self.output_path = "data/"+ output + ".txt"
        self.output = output
        self.debug = debug
        if not os.path.exists("build"):
                os.makedirs("build")

        if os.path.exists("build/execute_{0}".format(output)):
            self.__compile("rm build/execute_{0}".format(output))
        if self.debug:
            print("{} {} -o execute_{} {}".format(compiler, parameter, output, filename))
        self.__compile("{} {} -std=c++11 -o execute_{} {}".format(compiler, parameter, output, filename))
        self.__compile("mv execute_{0} build/execute_{0}".format(output))
            
    def run(self, MAX_ROW, MAX_COL):
        if os.path.exists(self.output_path):
            self.__compile("rm {}".format(self.output_path))
        
        for i in range(self.nTimes):
            nCol, nRow = random.randint(0,MAX_ROW-1), random.randint(0,MAX_COL-1)
            if self.debug: 
                print("./build/execute_{} {} {}  >> {}" .format(self.output, nCol, nRow, self.output_path))
                self.__compile("./build/execute_{} {} {}  >> {}" .format(self.output, nCol, nRow, self.output_path))
            else:
                self.__compile("./build/execute_{} {} {} | grep -A 1 Timer | grep ^[0-9] >> {}"
                    .format(self.output, nCol, nRow, self.output_path))
                    
    def __compile(self, commond):
        sp.call(commond, shell=True)   

class vis(object):
    def __init__(self, param):
        self.__compile("Rscript vis.R {} {} {} {}".format(*param["path"], *param["names"]))

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

if __name__ == "__main__":
    # Config
    with open('config.json') as json_file:
        config = json.load(json_file)
    
    outputs = {
        1:["Unroll", "Non-Unroll"],
        2:["Unroll-option", "Non-Unroll-option"],
        3:["unroll", "non_unroll"]
    }

    params = {
        1:"",
        2:"-funroll-loops",
        3:""
    }

    filenames = ["non-unroll.cpp", "unroll.cpp"]
    
    problem, num_loop, compiler, debug =  config.values()
    output = outputs[problem]
    param = params[problem]

    data_files = {
        "path":[],
        "names":[]
    }
    
    for i in range(2):
        MAX_ROW, MAX_COL = getShape(filenames[i])
        builder = Build(filenames[i], num_loop, compiler, param, output[i], debug)
        builder.run(MAX_ROW, MAX_COL)
        data_files["path"].append(builder.output_path)
        data_files["names"].append(builder.output)
    
    plotter = vis(data_files)

    