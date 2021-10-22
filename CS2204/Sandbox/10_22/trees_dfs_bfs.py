# -*- coding: utf-8 -*-
"""
Created on Fri Oct 22 10:48:42 2021

@author: kdmen
"""

from collections import deque


class Node:
    def __init__(self, data):
        self.data = data
        self.children = []

    def __repr__(self):
        return str(self.data)


def dfs(roots):
    # Depth first search
    stack = deque()
    stack.append(root)
    while stack:
        node = stack.pop()
        print(node)
        for child in node.children[::-1]:
            # [::-1] e.g. go left to right
            # Without this it goes right to left
            # Just reverses the children list
            stack.append(child)


def dfs_recursive(node):
    print(node)
    for child in node.children:
        dfs_recursive(child)


def bfs(root):
    queue = deque()
    queue.appendleft(root)
    while queue:
        node = queue.pop()
        print(node)
        for child in node.children:
            queue.appendleft(child)


if __name__ == '__main__':
    root = n1 = Node(1)

    n2 = Node(2)
    n3 = Node(3)
    n4 = Node(4)
    n1.children.append(n2)
    n1.children.append(n3)
    n1.children.append(n4)

    n5 = Node(5)
    n6 = Node(6)
    n2.children.append(n5)
    n2.children.append(n6)

    dfs(root)
    print("----")
    bfs(root)
    print("----")
    dfs_recursive(n1)
