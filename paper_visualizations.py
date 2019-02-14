# -*- coding: utf-8 -*-
"""
Created on Tue Feb 12 14:27:24 2019

@author: jdbul
"""


"""

Run this after reading in data from the initial file.  This is 
only visualization for paper

"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


#%%

df = crash_data_raw
 
# Basic 2D density plot
sns.set_style("white")
sns.kdeplot(df.LONGITUDE, df.LATITUDE)
#sns.plt.show()
 
# Custom it with the same argument as 1D density plot
sns.kdeplot(df.LONGITUDE, df.LATITUDE, cmap="Reds", shade=True, bw=.15)
 
# Some features are characteristic of 2D: color palette and wether or not color the lowest range
sns.kdeplot(df.LONGITUDE, df.LATITUDE, cmap="Blues", shade=True, shade_lowest=True, )
sns.plt.show()
