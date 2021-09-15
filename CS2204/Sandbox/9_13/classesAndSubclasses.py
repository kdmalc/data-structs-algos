# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 10:42:32 2021

@author: malcolkd
"""

from math import sqrt

class Point:
    """Represents a point in 2D"""
    origin = (0, 0)

    def __inint__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def distance(self):
        return sqrt(self.x**2 + self.y**2)

class NamePoint(Point):
    def __init__(self, x=0, y=0, name""):
        super().__init(x, y)
        self.name = name

    def __repr__(self):
        return f"({self.name}: {self.x}, {self.y})"

if __name__ == "__main__":
    print(Point.origin)

    p1 = Point(2,3)
    print(p1.distance())

    p2 = NamePoint(5,6,"Point 2")
    print(p2.distance())
        