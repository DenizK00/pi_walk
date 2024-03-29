#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 11 10:30:32 2023

@author: deniz
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import mpmath
import argparse


class DigitStick:
    def __init__(self, digit, theta, color, coloring, prev=None):
        self.digit = digit
        self.theta = theta
        self.r = 0
        self.color = color
        self.coloring = coloring
        self.prev = prev
        self.next = None

    def area_shoelace(self, old):
        v1 = polar_to_cartesian(self.prev.r, self.prev.theta)
        v2 = polar_to_cartesian(self.r, self.theta)
        v3 = polar_to_cartesian(self.next.r, self.next.theta)
        v4 = polar_to_cartesian(old.r, old.theta)

        coords = [v1, v2, v3, v4]
        sum_area = 0
        for i in range(len(coords)):
            m = np.array([coords[i%len(coords)], coords[(i+1)%len(coords)]]).T
            area = np.linalg.det(m)
            sum_area += area

        return abs(round(sum_area/2, 2))


    def render(self, ax, rendering, old, alpha):
        if self.coloring == "random":
            ax.scatter(self.theta, self.r, zorder=2)
        else:
            ax.scatter(self.theta, self.r, c=self.color, zorder=2)

        if "l" in rendering:
            thetas = [self.prev.theta, self.theta, self.next.theta]
            rs = [self.prev.r, self.r, self.next.r]

            ax.plot(thetas, rs)

            if "a" in rendering:
                thetas.append(old.theta)
                rs.append(old.r)

                ax.fill(thetas, rs, alpha=alpha)

    def copy(self):
        new_ds = DigitStick(self.digit, self.theta, self.color, self.coloring)
        new_ds.r = self.r
        return new_ds


def digit_arc(digit, offset_r) -> float:
    return offset_r + digit*math.pi/5


def cartesian_to_polar(x, y):
    r = np.sqrt(x**2 + y**2)
    theta = np.arctan(y/x)
    return (r, theta)


def polar_to_cartesian(r, theta):
    x = r*np.cos(theta)
    y = r*np.sin(theta)
    return np.array([x, y])


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


def update_result(result:pd.DataFrame, number:str, digitSticks:list[DigitStick], approximation, area_total, area_delta) -> pd.DataFrame:
    current = {str(i) + "_freq":int(digitSticks[i].r/0.5) for i in range(10)}
    areas = {"area_total":area_total, "area_delta":area_delta}
    current.update(areas)
    current[number] = approximation

    result.append(current)
    return result


def main(number:str, precision:int, offset:float, coloring:str, speed:float, rendering:str):
    mpmath.mp.dps = precision+1
    offset_radian = np.deg2rad(offset)

    if number == "pi":
        digits = str(mpmath.mp.pi)
    elif number == "e":
        digits = str(mpmath.mp.e)
    elif number == "phi":
        digits = str(mpmath.mp.phi)

    colors = ['blue', 'orange', 'green', 'red', 'purple', 'brown', 'pink', 'gray', 'olive', 'cyan']
    colors = ["tab:"+c for c in colors]

    fig = plt.figure(figsize=(12, 6))
    walk_ax = fig.add_subplot(121, projection="polar")  # Polar projection for the first subplot
    bar_ax = fig.add_subplot(222) # Subplot for barchart
    area_ax = fig.add_subplot(224) # Subplot for area plot

    walk_ax.set_title("Walk")
    bar_ax.set_title("Digit Distribution")
    area_ax.set_title("Area")

    walk_ax.set_yticklabels([])
    angle_labels = [str((i+1)%10) for i in range(10)]
    walk_ax.set_xticks(np.pi/5. * np.linspace(1, 10, 10))
    walk_ax.set_xticklabels(angle_labels)
        
    digit_sticks = init_render(offset, colors, coloring)

    result = []
    digitFreqs= [0] * 10
    bar_ax.grid()
    area_total = [0]
    area_deltas = []
    area_alphas = []
    delta_colors = []
    approximations = [digits[:2]]

    for c in digits[2:]:
        approximations.append(approximations[-1]+c)
        i = int(c)
        ds = digit_sticks[i]
        old_ds = ds.copy()
        ds.r += 0.5
        digitFreqs[i] += 1

        area_delta = ds.area_shoelace(old_ds)
        area_deltas.append(area_delta)
        area_alphas.append(area_delta*100)
        area_total.append(area_total[-1]+area_delta)
        delta_colors.append(colors[i])

        bar_ax.bar([str(ds.digit) for ds in digit_sticks], digitFreqs, color=colors, zorder=2)
        area_ax.scatter(np.linspace(1, len(area_total[1:]), len(area_total[1:])), area_total[1:], s=area_alphas, alpha=0.314, c=delta_colors)
        ds.render(walk_ax, rendering, old_ds, min(area_delta/3.1415, 1))
        fig.suptitle(number+" walk precision:" + str(len(area_deltas)) + "\n" + approximations[-1])

        result = update_result(result, number, digit_sticks, approximations[-1], round(area_total[-1], 4), area_deltas[-1])
        print(f"Progress: {round(100*len(area_deltas)/precision, 2)}%")

        plt.draw()
        plt.pause(1/(1.3142*speed))

    result_df = pd.DataFrame(result)
    result_df.to_csv("output/" + number + "_walk_" + str(precision) +".csv")
    plt.savefig("output/" + number + "_walk_" + str(precision) +".png", dpi=1200)

    plt.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--number", help="number to approximate: pi, e or phi", type=str, default="pi")
    parser.add_argument("-p", "--precision", help="pi approximation precision limit", type=int, default=100)
    parser.add_argument("-o", "--offset", help="visualization offset (Degrees)", type=float, default=0)
    parser.add_argument("-c", "--coloring", help="random/digitwise", type=str, default="digitwise")
    parser.add_argument("-s", "--speed", help="rendering speed default:1.5", type=float, default=1.5)
    parser.add_argument("-r", "--rendering", help="Rendering setting: l for lines, a for area, None for only points ", default="la") # Rendering Setting
    args = parser.parse_args()

    main(number=args.number, precision=args.precision, offset=args.offset, coloring=args.coloring, speed=args.speed, rendering=args.rendering)


