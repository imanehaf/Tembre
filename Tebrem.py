# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 16:37:09 2015

@author: imanies
"""

import matplotlib.pyplot as pl
import numpy as np
from sklearn import linear_model
from os.path import join, isfile
from os import listdir
import collect 

def main(src, cfg_h, cfg_t): #src is path to executables
    exe_files = [ f for f in listdir(src) if isfile(join(src,f)) ]
    host = collect.Collect()
    target = collect.Collect()
    #Execution times of executables run on HOST computer
    hData = host.zsimCall(src, exe_files, cfg_h)

    #Execution times of executables tun on TARGET computer
    tData = target.zsimCall(src, exe_files, cfg_t)
    return hData, tData

def display(data):
    pd = np.array(data[1].values())
    zd = np.array(data[0].values())
    regr = linear_model.LinearRegression()
    
    zd_x = zd[:, np.newaxis]
    pd_x = pd[:, np.newaxis]

    regr.fit(pd_x, zd_x)
    
    pl.scatter(pd, zd,  color='black')
    pl.plot(pd_x, regr.predict(pd_x), color='red', linewidth=2)
    
    pl.show()