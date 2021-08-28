# -*- coding: utf-8 -*-
"""
Created on Fri Aug 27 10:43:24 2021

@author: 14193

8_27_21
In class, not submitted
Estimating Pi via the Monte Carlo method:
    
"""

from random import random

# Version 1: init
N = 1_000_000
n_in = 0
for _ in range(N):
    # He used "_" as the var name since we won't be using it
    x, y = random(), random() # More Pythonic form of dual assignment
    r2 = x**2 + y**2
    if r2 < 1.0:
        # Keep track of how many points fall within the unit circle
        n_in += 1
        
# Version 2: Condensed for loop
N = 1_000_000
n_in = 0
for _ in range(N):
    # He used "_" as the var name since we won't be using it
    x, y = random(), random() # More Pythonic form of dual assignment
    if x**2 + y**2 < 1.0:
        # Keep track of how many points fall within the unit circle
        n_in += 1

# A VERY SIMPLE FOR LOOP USUALLY SUGGESTS LIST COMPREHENSION CAN BE USED

# Version 3: List comprehension
N = 1_000_000
n_in = sum([random()**2 + random()**2 < 1 for _ in range(N)])
        
# Formula: k/N * 4 = Pi
print(n_in / N * 4)

# Version 4: Function so that we can parametrize it
def pi(N=1_000_000):
    n_in = sum([random()**2 + random()**2 < 1 for _ in range(N)])
    return (n_in / N * 4)
    
print(pi())