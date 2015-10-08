# -*- coding: utf-8 -*-
"""
Created on Tue Jul  7 07:44:47 2015

@author: imanies
"""

import matplotlib.pyplot as plt
import numpy as np
parsec={'Blachscholes': 765649,  'Freqmine':22537259,  'Raytrace':3857564,'Swaptions': 1908575}
host_pred=[2336557,
          978642,
        26845584,
         4652159]
       
     
host_real = [2353427, 970472, 21407094, 5476320 ]
std = [2353427*1.22/100, 970472*0.73/100, 21407094*0.39/100, 5476320*1.14/100]
fig = plt.figure()
ax = fig.add_subplot(111)
ind = np.arange(4)                # the x locations for the groups
width = 0.35
rects1 = ax.bar(ind, host_real, width,
                color='black',
                yerr = std,
                error_kw=dict(elinewidth=2,ecolor='red'))

rects2 = ax.bar(ind+width, host_pred, width,
                    color='orange',
                    error_kw=dict(elinewidth=2,ecolor='black'))
                    
ax.set_xticks(ind+width)
xtickNames = ax.set_xticklabels(parsec.keys())
plt.setp(xtickNames, rotation=45, fontsize=10)
                    
ax.legend( (rects1[0], rects2[0]), ('Real', 'Predicted') )
ax.set_ylabel('# of Cycles')
plt.show()