#!/usr/bin/python


'''
@Author: Lin Sinan
@Github: https://github.com/linsinan1995
@Email: mynameisxiaou@gmail.com
@LastEditors: Lin Sinan
@Description: 
              
'''

import argparse
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
    python_int = "python"
    
    Run(args.nlab, python_int)