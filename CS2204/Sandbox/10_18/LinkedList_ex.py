# -*- coding: utf-8 -*-
"""
Created on Mon Oct 18 10:35:09 2021

@author: kdmen
"""


class Node:
    def __init__(self, value):
        self.data = value
        self.next = None


class LinkedList:
    # One implementation of a double ended queue
    def __init__(self):
        self.head = None

    def appendleft(self, value):
        new_node = Node(value)
        new_node.next = self.head
        # ^Points to the current front of the LL
        self.head = new_node
        # ^Now this node is the first node, so update the head

        # Don't need to return this, but doing so allows us to
        #  chain .appendleft() commands on one line
        return self

    def popleft(self):
        if self.head is None:
            raise IndexError("Cannot popleft from empty list")

        value = self.head.data
        self.head = self.head.next
        return value

    def append(self, value):
        if self.head is None:
            self.head = Node(value)

        node = self.head()
        while node.next:
            node = node.next
        node.next = Node(value)

        return self


if __name__ == "__main__":
    # This is a stack
    lst = LinkedList()
    lst.appendleft(1).appendleft(2).appendleft(3)
    print(lst.popleft())
    print(lst.popleft())
    print(lst.popleft())
