from collections import deque

stack = deque()
# dir(stack) returns all the possible methods usuable with this
stack.append("cnn")
stack.append("/india")
stack.append("/china")
print(stack)

# Creating a proper stack class (normally would just use deque())
class Stack:
    def __init__(self):
        self.container = deque()

    def push(self, val):
        self.container.append(val)

    def pop(self):
        return self.container.pop()

    def peek(self):
        return self.container[-1]

    def is_empty(self):
        return len(self.container)==0

    def size(self):
        return len(self.container)

s = Stack()
s.push(5)
print(s.peek())
s.pop()
print("Just ran pop, are we now empty?")
print(s.is_empty())