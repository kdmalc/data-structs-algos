# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 11:05:50 2021

@author: kdmen
"""


from threading import Thread
from time import sleep


def worker():
    print("Start")
    while True:
        print("Loop")
        sleep(1.1)


if __name__ == "__main__":
    t = Thread(target=worker)
    t.start()

    while True:
        print("Main")
        sleep(3.2)
