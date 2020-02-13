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
from scipy.stats import ttest_ind, probplot
from scipy.stats import kstest

import math

datas = []
compilers = ["gcc", "icc"] # "gcc", "clang",
df = pd.DataFrame(columns=compilers)
for cpl in compilers:
    path =  "data/" + cpl + ".txt"
    data = np.loadtxt(path)
    datas.append(data)
    df[cpl] = data

print(kstest(df["icc"], 'norm'))
# print(ttest_ind(df["gcc"], df["icc"], equal_var=False))
df["icc"].plot(kind='hist', title= 'Blood Pressure Difference Histogram')
plt.show()