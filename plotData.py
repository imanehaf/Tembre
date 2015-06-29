# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 16:37:09 2015

@author: imanies
"""

import matplotlib.pyplot as pl
import numpy as np
from sklearn import linear_model

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