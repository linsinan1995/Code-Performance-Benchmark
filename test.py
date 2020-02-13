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


def t_test(data, cplName1, cplName2, alpha = 0.05, save_pic = True):
    
    print("Hypothesis 0: compiler {0} is faster or equal to compiler {1}, \nHypothesis 1: compiler {0} is slower than compiler {1}".format(cplName1, cplName2))
    # print("Hypothesis 0: compiler {0} is >= to compiler {1}, \nHypothesis 1: compiler {0} is < compiler {1}".format(cplName1, cplName2))
    t_value, p = ttest_ind(data[cplName1], data[cplName2], equal_var=False)

    diff = data[cplName1] - data[cplName2]
    df = len(data)-1 # degree of freedom

    t_alpha_percentile = t.ppf(alpha / 2, df)

    print("P value is {}, t value is {}".format(p/2, t_value))
    if (p/2 < alpha and t_value > 0):
        print("REJECT the null hypothesis\n")
    else:
        print("ACCEPT the null hypothesis\n")


    rv = t(df)
    limit = np.minimum(rv.dist.b, 5)
    x = np.linspace(-1 * limit, limit)
    h = plt.plot(x, rv.pdf(x), label = 'Student\'s t distribution')
    plt.xlabel('x')
    plt.ylabel('t(x)')
    plt.title('Difference significance test -- {} v.s. {}'.format(cplName1, cplName2))
    plt.grid(True)
    plt.axvline(x = t_alpha_percentile, ymin = 0, ymax = 0.095, 
            linewidth=2, color='r', label = '($\\alpha$ / 2) percentile')
    plt.axvline(x = t_value, ymin = 0, ymax = 0.6, 
            linewidth=2, color='g', label = 't value')

    plt.annotate('$\\alpha$ / 2 percentile', xy = (t_alpha_percentile, 0.05),
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
    if save_pic:
        if not os.path.exists("pics"):
            os.makedirs("pics")
        plt.savefig('pics/result.png')
    plt.show()

if __name__ == "__main__":
    compilers = ["javac", "clang", "gcc", "icc"]
    data = pd.DataFrame(columns=compilers)

    for cpl in compilers:
        path =  "data/" + cpl + ".txt"
        dat = np.loadtxt(path)
        data[cpl] = dat
    
    for i in range(len(compilers)):
        for j in range(i+1, len(compilers)):
            t_test(data, compilers[i], compilers[j], alpha = 0.05)
    
    