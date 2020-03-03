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
import json
import subprocess as sp
import itertools

class Build(object):
    def __init__(self, filename, nTimes, compiler, parameter, output, debug = False):
        self.nTimes = nTimes
        self.compiler = compiler
        self.output_path = "data/"+ output + ".txt"
        self.output = output
        self.debug = debug
        
        if os.path.exists("build/execute_{0}".format(output)):
            self.__compile("rm build/execute_{0}".format(output))
        if self.debug:
            print("{} {} -std=c++11 -o execute_{} {}".format(compiler, parameter, output, filename))
        self.__compile("{} {} -std=c++11 -o execute_{} {}".format(compiler, parameter, output, filename))
        self.__compile("mv execute_{0} build/execute_{0}".format(output))
            
    def run(self, MAX_ROW, MAX_COL):
        if os.path.exists(self.output_path):
            self.__compile("rm {}".format(self.output_path))
        
        for i in range(self.nTimes):
            nCol, nRow = random.randint(0,MAX_ROW-1), random.randint(0,MAX_COL-1)
            if self.debug: 
                print("./build/execute_{} {} {}  >> {}" .format(self.output, nCol, nRow, self.output_path))
            self.__compile("./build/execute_{} {} {} | grep -A 1 Timer | grep ^[0-9] >> {}" # 
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
    if not os.path.exists("build"):
            os.makedirs("build")
    
    if not os.path.exists("data"):
        os.makedirs("data")

    if not os.path.exists("pic"):
        os.makedirs("pic")

    # Config
    with open('config.json') as json_file:
        config = json.load(json_file)
    
    outputs = {
        1:["Unroll", "Non-Unroll", "Unroll-option", "Non-Unroll-option"],
        2:[i+j+z+opt  for opt in ["-int", "-int-opt" ] for i,j,z in  itertools.permutations("NMP", 3)],
        3:[i+j+z+"-till"  for i,j,z in  itertools.permutations("NMP", 3)]+ ["Best-tile-opt", "Normal-tile-2opt"]
    }
    
    # ['-D NMP -O2', '-D NPM -O2', '-D MNP -O2', '-D MPN -O2', '-D PNM -O2', '-D PMN -O2', '-D NMP -O2 -floop-interchange', 
    # '-D NPM -O2 -floop-interchange', '-D MNP -O2 -floop-interchange', '-D MPN -O2 -floop-interchange', '-D PNM -O2 -floop-interchange', '-D PMN -O2 -floop-interchange']
    
    params = {
        1:[ i+" -O2" for i in ["-D UNROLL", "", " -D UNROLL -funroll-loops", " -funroll-loops"]  ],
        2:["-D " + i+j+z+opt  for opt in [" -O2", " -O2 -floop-interchange" ] for i,j,z in  itertools.permutations("NMP", 3)],
        3:["-D " + i+j+z+" -O2"  for i,j,z in  itertools.permutations("NMP", 3)] + ["-D BEST_INT -O2 -floop-block", "-D NORMAL -O2 -floop-block  -floop-interchange"]
    }

# [i+j+z  for i,j,z in  itertools.permutations("NMP", 3)] # in output
# ["-D TEST -D " + i+j+z+" -O2"  for i,j,z in  itertools.permutations("NMP", 3)] # in params for test


    filenames = {
                                1:"unroll.cpp", 
                                2:"interchange.cpp",
                                3:"tiling.cpp"
                            }
                            
    problem, num_loop, compiler, debug, just_plot =  config.values()

    data_files = {
        "path":[],
        "names":[]
    }

    
    if not just_plot:
        for p in problem:
            output = outputs[p]
            param = params[p]
            filename = filenames[p]
            MAX_ROW, MAX_COL = getShape(filename)
            for i in range(len(param)):
                builder = Build(filename, num_loop, compiler, param[i], output[i], debug)
                builder.run(MAX_ROW, MAX_COL)
                data_files["path"].append(builder.output_path)
                data_files["names"].append(builder.output)

