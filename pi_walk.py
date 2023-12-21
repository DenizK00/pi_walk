#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 14:03:44 2023

@author: deniz
"""

import matplotlib.pyplot as plt
import numpy as np
import decimal
from dataclasses import dataclass, field

@dataclass
class digitContainer:
    i: int
    freq: int = field(default_factory=int)
    
def arange(start, stop, step):
    my_list = []

    while start < stop:
        my_list.append(start)
        start += step

    return my_list

def generateDC():
    dcs = []
    for i in range(10):
        dcs.append(digitContainer(i))
    return dcs


dcs = generateDC()
rs = []
degs = []

colors = ["red", "green", "orange"]
colors = colors * (10 // len(colors)) + colors[:10 % len(colors)]
i = 0

for i, r in enumerate(arange(0, 4, 0.05)):
    ci = np.random.randint(3)
    deg = 30 + r*(1 + min((i*20), 1000))
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})

    rs.append(r)
    degs.append(np.deg2rad(deg))
    ax.set_title("Experiment", va='bottom')
    ax.plot(degs, rs, marker="o", color=colors[ci], markersize=8)
    ax.set_rmax(4)
    ax.set_rticks([0.5, 1, 1.5, 2])  # Less radial ticks
    ax.set_rlabel_position(-22.5)  # Move radial labels away from plotted line 
    ax.grid(True)       
    plt.pause(0.001)
    
    


