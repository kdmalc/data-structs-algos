# -*- coding: utf-8 -*-
"""
Created on Wed Dec  1 10:43:31 2021

@author: malcolkd
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim
from scipy.signal import convolve2d


arena = np.random.choice([1, 0], p=[0.2, 0.8], size=(100, 100))
kernel = np.array(
    [
     [1, 1, 1],
     [1, 0, 1],
     [1, 1, 1],
     ]
    )

# plt.imshow(arena, cmap="Greys")
# White is dead, black is live. ~20% are alive


# Replacing the above with an actual animation
def step(frame_num):
    # Mode and boundary take care of padding (let us do a conv on the edges)
    neighbors = convolve2d(arena, kernel, mode="same", boundary="wrap")
    # Kill the cells based on Conway's rules
    arena[neighbors != 2] = 0
    # Make cells alive based on Conway's rules
    arena[neighbors == 3] = 1
    image.set_data(arena)


# WRITE <%matplotlib qt> IN CONSOLE SO THAT ANIMATION IS IN ITS OWN WINDOW
fig, ax = plt.subplots()
image = ax.imshow(arena, cmap="Greys")
animation = anim.FuncAnimation(fig, step, interval=30)
plt.show()
