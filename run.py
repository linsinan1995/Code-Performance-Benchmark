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

class Run(object):
    def __init__(self, which_lab, python):
        self.__compile("cd src/lab{} ; {} build.py".format(which_lab, python)) 

    def __compile(self, commond):
        sp.call(commond, shell=True)        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter times of executing')
    parser.add_argument('-lab', '--nlab', type=int, default = 1)
    args = parser.parse_args()

    if args.nlab < 1:
        args.nlab = 1
        
    # Config
    python_int = "python3"
    
    Run(args.nlab, python_int)