#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 14:09:04 2021

@author: gh
"""
'''
For graphing of PMF maps generated with wham.pl
'''

from collections import defaultdict
from collections import OrderedDict
import pprint
import numpy as np
import sys
import os
import re
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import ticker

'''
Options
'''
in_fn = '2dpmf.dat'
xlabel = 'Q value'
ylabel = 'Num. of hydrogen bonds'
cblabel = 'Free energy (kcal/mol)'
out_fn = 'pmf.eps'

'''
Data import
'''

with open(in_fn, 'r') as data_file:
    data = data_file.readlines()
    data_mat = np.array([ [ float(x) for x in re.split(" +", s) if x!='\n' ] for s in data ])
    # print(data_mat)
    data_file.close()

x,y = (data_mat[:,0],data_mat[:,1])
z = data_mat[:,2]

'''
Set cutoff of levels
'''
cutoff = np.min(z) + 9
for i in range(z.size):
    if z[i] > cutoff:
        z[i] = cutoff

print(np.max(z),np.min(z))

'''
Make x, y, z for graphing
'''

x_plt = np.unique(x)
y_plt = np.unique(y)
z_plt = np.zeros((x_plt.size, y_plt.size))


for data_pt in data_mat:
    i, = np.where(x_plt == data_pt[0])
    j, = np.where(y_plt == data_pt[1])
    # print(i,j)
    z_plt[i[0]][j[0]] = data_pt[2]
    
#print('z_plt = ', z_plt)
    
print(y_plt.size,x_plt.size)

print(z_plt[0].size)

'''
Graphing
'''
# Set graph labels

fib, ax = plt.subplots()

# Set upper bounds and aspect ratio
y_upper = 40

#ax.set_aspect( (np.max(x_plt) - np.min(x_plt)) / (np.max(y_plt) - np.min(y_plt)) )
ax.set_aspect( 1 / y_upper )

norml = mpl.colors.Normalize(vmin=np.min(z),vmax=np.min(z)+6.01)
# levs = np.arange(np.min(z),np.max(z),0.6)
levs = np.arange(np.min(z),np.min(z)+6.01,0.6)
print(levs)

print(type(z_plt), z_plt.shape)


# levs = np.insert(np.arange(np.min(z),np.max(z),0.6), 0, np.min(z), axis = 0)

filling = plt.contourf( x_plt, y_plt, np.transpose(z_plt), cmap = 'jet', norm = norml, levels = levs)

# Label font
lfont = {'fontname':'Times New Roman', 'size': '20'}

# Axis labels
# plt.xlabel(xlabel, **lfont, fontsize=16)
# plt.ylabel(ylabel, **lfont, fontsize=16)

# Axis ranges
plt.xlim([-0.02,1.02])
plt.ylim([-1,y_upper])

# Axis ticks
# ax.set_xticks([0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1])
# ax.set_yticks(list(range(0,25,2)))

plt.xticks([0, 0.2, 0.4, 0.6, 0.8, 1], **lfont)
plt.yticks(ticks = list(range(0,y_upper+1,4)), labels = list(range(0,y_upper+1,4)), **lfont)

# Colorbar
lfont_cb = {'fontname':'Times New Roman', 'size': '16'}
font = mpl.font_manager.FontProperties(family='times new roman', size=20)
levs_sig_digits = np.around(levs-np.min(levs), decimals = 1)
print(levs_sig_digits)
cb = plt.colorbar(label = cblabel)
cb.set_ticks(levs)
# cb.set_ticklabels(levs_sig_digits)
cb.ax.set_yticklabels(levs_sig_digits, **lfont_cb)
cbtext = cb.ax
cbtext.yaxis.label.set_font_properties(font)
for l in cb.ax.yaxis.get_ticklabels():
    l.set_family("Times New Roman")



'''
Write to file
'''

out_dir = './'
plt.savefig(out_dir + out_fn, dpi = 400)

plt.show()
