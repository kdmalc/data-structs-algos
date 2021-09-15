# -*- coding: utf-8 -*-
"""
Color Management Library for Rainbow, Inc.

How to implement a class that can represent color
Here, every color is represented by RGB, which is sort of how the eye works
RGB is additive

Created on Mon Sep 13 10:51:36 2021

@author: malcolkd
"""

import matplotlib.pyplot as plt

class Color:
    """Simple color data structure with RGB values"""

    def __init__(self, red, green, blue):
        # Uses 1 line to bound red between 0 and 1
        # Sanity checking / pruning can be done in the INIT function
        # Want to catch invalid data early
        self.r = max(min(red, 1.0), 0.0)
        self.g = max(min(green, 1.0), 0.0)
        self.b = max(min(blue, 1.0), 0.0)

    def __repr__(self):
        return f"Color({self.r}, {self.g}, {self.b})"

    def __add__(self, other):
        return Color(self.r + other.r,
                     self.g + other.g,
                     self.b + other.b
                     )

    def show(self):
        # %matplotlib qt
        plt.figure(repr(self), facecolor=(self.r, self.g, self.b))

class NamedColor(Color):

    # Instead of having very long if statements, use a dictionary
    # E.g. avoid (if name==red, elif name==bue, etc)

    # E.g. look up table
    lut = {
        "navy": (0, 0, 0.5),
        "yellow": (1, 1, 0)}

    def __init__(self, name):
        r, g, b = self.lut[name]
        super().__init__(r, g, b)
