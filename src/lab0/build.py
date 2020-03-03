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
    def __init__(self):
        self.__compile("javac Matrix.java")
    def run(self, output_path, option):
        if os.path.exists(output_path):
            self.__compile("rm {}".format(output_path))
        for i in range(30):
            nCol, nRow = random.randint(0,500-1), random.randint(0,500-1)
            print("java {} Matrix  {} {} | grep -A 1 Timer | grep ^[0-9] >> {}" .format(option, nCol, nRow, output_path))
            self.__compile("java {} Matrix  {} {} | grep -A 1 Timer | grep ^[0-9] >> {}" .format(option, nCol, nRow, output_path)) # 
                    
    def __compile(self, commond):
        sp.call(commond, shell=True)   

if __name__ == "__main__":
    if not os.path.exists("data"):
        os.makedirs("data")
    options= ["-XX:CompileThreshold=1 -XX:TieredStopAtLevel=2", 
                         "-XX:CompileThreshold=1 -XX:TieredStopAtLevel=4", 
                         "-XX:+TieredCompilation", 
                         "-XX:CompileThreshold=1 -XX:+TieredCompilation", 
                         "-XX:CompileThreshold=1 "]
    output = ["data/client_matrix.txt",  
                        "data/server_matrix.txt", 
                        "data/tiered_matrix.txt", 
                        "data/tiered_1_matrix.txt", 
                        "data/no-flag_matrix.txt"]
    build = Build()
    for i in range(len(options)):
        build.run(output[i], options[i])