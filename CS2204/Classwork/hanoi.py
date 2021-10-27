"""Recursive solution for the Towers of Hanoi"""
import turtle
import random
from collections import deque
from itertools import permutations
from random import choice

'''
# Importing the desired file
# This was run in the console

import urllib
urllib.request.urlretrieve("http://cs2204.org/hanoi.py", "hanoi.py")
# ^ 2nd argument is the name of the file to be stored locally
'''


### YOUR CODE BEGINS HERE #####################################################
def solve_random(t1, t2, t3):
    # Move the discs completely randomly
    # But code up the rules of the game
    # Arbitrary, legal moves

    while t1 or t2:
        # ^Eg all the discs are on t3
        valid_moves = []
        # All potential source and destinations
        for src, dst in permutations([t1, t2, t3], 2):
            if src and (dst.top() > src.top() or dst.is_empty()):
                valid_moves.append( (src, dst) )
        src, dst = choice(valid_moves)
        dst.push(src.pop())


def solve_recursive(n, t1, t2, t3):
    if n < 1:
        return

    solve_recursive(n - 1, t1, t3, t2)
    t3.push(t1.pop())
    solve_recursive(n - 1, t2, t1, t3)


def solve(t1, t2, t3):
    """Solve the Tower of Hanoi game by moving the discs.

    The parameters t1, t2 and t3 are three stacks, supporting the following
    methods:
        disc = t<n>.pop()      - remove the top most disc from the tower
        t<n>.push(disc)        - placing a disc on the top of the tower
        disc = t<n>.top()      - looking (nor removing) the top most disc
        t<n>.is_empty()        - true if there are no discs on the tower
    """

    '''
    # How to shuffle discs at all
    t3.push(t1.pop())
    # Push and pop discs to move them
    '''
    
    '''
    # Basic human solution
    t3.push(t1.pop())
    t2.push(t1.pop())
    t2.push(t3.pop())
    t3.push(t1.pop())
    # etc etc
    '''

    # solve_random(t1, t2, t3)
    solve_recursive(6, t1, t2, t3)


### YOUR CODE ENDS HERE #######################################################


class Disc(turtle.Turtle):
    """Represent a single disc on the tower"""

    def __init__(self, n):
        super().__init__(shape="square", visible=False)
        self.n = n
        self.penup()
        self.shapesize(1.5, n*1.5, 2)  # square-->rectangle
        self.fillcolor(n/6., 0, 1-n/6.)
        self.showturtle()
        self.speed('fast')

    def __lt__(self, other):
        return self.n < other.n


class Tower(deque):
    "Hanoi tower, a subclass of deque, implementing stack logic"

    def __init__(self, n):
        "create an empty tower. x is x-position of peg"
        super().__init__()
        self.n = n

    def push(self, d):
        if len(self) and d > self.top():
            raise ValueError("cannot push larger disc on smaller one")
        super().append(d)
        d.setx(self.n * 250 - 500)
        d.sety(-150+34*len(self))

    def pop(self):
        d = super().pop()
        d.sety(150)
        return d

    def top(self):
        return self[-1]

    def is_empty(self):
        return len(self) == 0


def main():
    screen = turtle.Screen()
    screen.setup(800, 600)
    rootwindow = screen.getcanvas().winfo_toplevel()
    rootwindow.call('wm', 'attributes', '.', '-topmost', '1')
    rootwindow.call('wm', 'attributes', '.', '-topmost', '0')

    turtle.hideturtle()
    turtle.penup()
    turtle.goto(0, -225)   # writer turtle

    t1 = Tower(1)
    t2 = Tower(2)
    t3 = Tower(3)

    n = 6  # make tower of 6 discs
    for i in range(n, 0, -1):
        t1.push(Disc(i))

    solve(t1, t2, t3)

    turtle.done()


if __name__ == "__main__":
    main()
