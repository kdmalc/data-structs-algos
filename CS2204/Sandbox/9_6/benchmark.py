# -*- coding: utf-8 -*-
"""
Created on Mon Sep  6 10:21:26 2021

@author: malcolkd
"""

from time import time
import numpy as np


def squares_loop(n):
    result = []
    for value in range(n):
        result.append(value**2)
    return result


# A more compact code
# Not that much time improvement, but improves code readability
def squares_comprehension(n):
    return [value**2 for value in range(n)]


# A more scientific computing approach:
def squares_numpy(n):
    return np.arange(n, dtype='int64') ** 2


if __name__ == "__main__":
    n = 1_000_000

    for func in (squares_loop, squares_comprehension, squares_numpy):
        t_begin = time()
        result = func(n)
        t_end = time()
        # Does it equal the closed form formula for the sum of n squares?
        assert sum(result) == (n - 1) * n * (2 * n - 1) // 6
        elapsed_ms = 1000.0 * (t_end - t_begin)
        # :<22 aligns 22 spaces to the left
        print(f"{func.__name__:<22}: {elapsed_ms:.3f} ms")
