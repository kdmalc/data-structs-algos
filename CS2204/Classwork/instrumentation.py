# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 10:34:03 2021

@author: malcolkd
"""

from time import time


# Wrapper/shell function
def time_this(fn):
    # Returns a wrapped function with timing capabilities

    def timer(*args, **kwargs):
        # E.g. catch all parameters
        begin = time()
        result = fn(*args, **kwargs)
        end = time()
        print(f"Execution time: {end - begin} seconds")
        return result
    return timer


@time_this
def is_prime(n):
    n = abs(n)
    if n < 2:
        return False

    for i in range(2, n):
        if n % i == 0:
            return False
    return True


if __name__ == "__main__":
    print(f"17: {is_prime(17)}")

    is_prime = time_this(is_prime)
    print(f"17: {is_prime(17)}")
    print(f"1717171: {is_prime(1717171)}")
