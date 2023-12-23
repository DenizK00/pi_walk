#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 10:30:32 2023

@author: deniz
"""

import decimal
import math
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import mpmath
import math
import argparse

class DigitStick:
    def __init__(self, digit, theta, color, coloring, prev=None, next=None):
        self.digit = digit
        self.theta = theta
        self.r = 0
        self.color = color
        self.coloring = coloring
        self.prev = prev

    def render(self, ax):
        if self.coloring == "random":
            ax.scatter(self.theta, self.r, zorder=2)
        else:
            ax.scatter(self.theta, self.r, c=self.color, zorder=2)

def digit_arc(digit, offset_r) -> float:
    return offset_r + digit*math.pi/5

def init_render(offset_radian, colors, coloring):
    digitSticks = [DigitStick(0, digit_arc(0, offset_radian), colors[0], coloring)]
    digit = 1
    while digit < 10:
        ds = DigitStick(digit, digit_arc(digit, offset_radian), colors[digit], coloring, prev=digitSticks[digit-1])
        digitSticks.append(ds)
        digit += 1

    for ds in digitSticks:
        ds.next = digitSticks[(ds.digit + 1) % 10]

    digitSticks[0].prev = digitSticks[-1]

    return digitSticks

def update_result(result:pd.DataFrame, digitSticks:list[DigitStick]) -> pd.DataFrame:
    current_freqs = {str(i) + "_freq":int(digitSticks[i].r/0.5) for i in range(10)}
    result.append(current_freqs)
    return result

def render_area(digitSticks: list[DigitStick],digit:int,  ax):
    i = 0
    while i < len(digitSticks)-1:
        ax.plot([digitSticks[i].theta, digitSticks[i+1].theta], [digitSticks[i].r, digitSticks[i+1].r])
        ax.fill([0, digitSticks[i].theta, digitSticks[i+1].theta], [0, digitSticks[i].r, digitSticks[i+1].r], alpha=0.5)
        i += 1
    # ax.plot([digitSticks[i].theta, digitSticks[i+1].theta], [digitSticks[i].r, digitSticks[i+1].r])



def main(number:str, precision:int, offset:float, coloring:str, speed:float):
    mpmath.mp.dps = precision
    offset_radian = np.deg2rad(offset)

    if number == "pi":
        digits = str(mpmath.mp.pi)[2:]
    elif number == "e":
        digits = str(mpmath.mp.e)[2:]
    elif number == "phi":
        digits = str(mpmath.mp.phi)[2:]


    colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    colors = ["tab:"+c for c in colors]

    # fig, (walk_ax, hist_ax) = plt.subplots(1, 2) #subplot_kw={'projection': 'polar'}
    fig = plt.figure(figsize=(12, 6))
    walk_ax = fig.add_subplot(121, projection="polar")  # Polar projection for the first subplot
    bar_ax = fig.add_subplot(122)  # Normal subplot
    fig.suptitle(number+" walk")

    walk_ax.set_yticklabels([])
    angle_labels = [str((i+1)%10) for i in range(10)]
    walk_ax.set_xticks(np.pi/5. * np.linspace(1, 10, 10))
    walk_ax.set_xticklabels(angle_labels)
        
    digit_sticks = init_render(offset, colors, coloring)

    # digit_sticks = [DigitStick(digit, digit_arc(digit, offset_radian), colors[digit], coloring) for digit in range(10)]

    result = []
    digitFreqs= [0] * 10
    bar_ax.grid()

    for c in digits:
        i = int(c)

        digitFreqs[i] += 1
        digit_sticks[i].r += 0.5
        digit_sticks[i].render(walk_ax)
        render_area(digit_sticks, i, walk_ax)

        bar_ax.bar([str(ds.digit) for ds in digit_sticks], digitFreqs, color=colors, zorder=2)

        result = update_result(result, digit_sticks)
        
        plt.draw()
        plt.pause(1/(1.3145*speed))

    result_df = pd.DataFrame(result)
    result_df.to_csv("output/" + number + "_walk_" + str(precision) +".csv")

    plt.close()


if __name__ == "__main__":
    # plt.style.use("seaborn-v0_8-darkgrid")

    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--number", help="number to approximate", type=str, default="pi")
    parser.add_argument("-p", "--precision", help="pi approximation precision limit", type=int, default=100)
    parser.add_argument("-o", "--offset", help="visualization offset (Degrees)", type=float, default=0)
    parser.add_argument("-c", "--coloring", help="random/digitwise", type=str, default="random")
    parser.add_argument("-s", "--speed", help="rendering speed", type=float, default=0.5)


    args = parser.parse_args()
    print(args.coloring)

    main(number=args.number, precision=args.precision, offset=args.offset, coloring=args.coloring, speed=args.speed)
        