# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 11:01:22 2021

@author: 14193
"""

from random import random


def monte_carlo(N=1_000_000):
    n_in = sum([random()**2 + random()**2 < 1 for _ in range(N)])
    return (n_in / N * 4)


def leibniz(N=1000):
    denomintor = 1.0
    sign = 1.0
    estimate = 0.0
    for _ in range(N):
        estimate += sign * 4 / denomintor
        denomintor += 2.0
        sign *= -1.0
    return estimate


if __name__ == "__main__":
    # Test cases
    n1 = 1000
    print(monte_carlo(n1))
    print(leibniz(n1))
