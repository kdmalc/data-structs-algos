# -*- coding: utf-8 -*-
"""
Created on Wed Oct 20 10:19:05 2021

@author: malcolkd
"""

# Grow a tree using a branch

from collections import deque
from math import radians, sin, cos
from time import sleep

# If it says Reloaded Module: Graphics, just restart the Kernel
# Cannot keep loading in the same module
# Therefore cannot run this file multiple times
# Eg must restart the kernel in between

try:
    from graphics import GraphWin, Point, Line
except ImportError:
    from urllib import request
    request.urlretrieve("http://cs2204.org/graphics.py", "graphics.py")
    from graphics import GraphWin, Point, Line

SIZE_X, SIZE_Y = 800, 600
SPAN = radians(30)
# ^All computers think about angles in radians

# USING A STACK, WE DRAW BOTTOM TO TOP
# THIS IS A DEPTH-FIRST ALGORITHM
# E.g. we draw everything so a single branch before moving onto the next one

# To chance to a queue, all we hae to do is change pop to popleft
# DRAWS TREE LAYER BY LAYER, RIGHT TO LEFT
# BREADTH-FIRST ALGORITHM

# Significant bias towards stacks, depth-first approach with recursion
# If you don't use a dequeue, intepretter has a stack-like logic ...
# as it keeps track of your function calls in recursion
# Thus recursion is implicitly depth-first


def draw_branches(win, start, length):
    # Using a stack, not a queue
    todo = deque()
    todo.append((start, length, 0))
    # ^ branch_start_point, branch_length, lean_angle

    while todo:
        start, length, ref_angle = todo.pop()
        for branch_angle in ref_angle + SPAN, ref_angle - SPAN:
            branch_end = Point(
                start.x + length * sin(branch_angle),
                start.y + length * cos(branch_angle)
                )
            branch = Line(start, branch_end)
            branch.draw(win)
            sleep(0.1)

            if length // 2 > 0:
                todo.append((branch_end, length // 2, branch_angle))


def draw_tree(win):
    length = 200  # pixels
    start = Point(0, -length)
    end = Point(0, 0)
    trunk = Line(start, end)
    trunk.draw(win)

    draw_branches(win, end, length // 2)


if __name__ == "__main__":
    win = GraphWin("Tree", SIZE_X, SIZE_Y)
    win.setCoords(-1 * SIZE_X // 2, -1 * SIZE_Y // 2, SIZE_X // 2, SIZE_Y // 2)
    # E.g. bottom left, bottom left, top right, top right

    # Draw an arbitrary line.  Demo
    # start = Point(0, 0)
    # end = Point(100, 200)
    # line = Line(start, end)
    # line.draw(win)

    draw_tree(win)

    win.getMouse()
    win.close()
