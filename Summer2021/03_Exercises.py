from collections import deque

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
        return len(self.container) == 0

    def size(self):
        return len(self.container)


# Exercise 1: reverse_string function
def reverse_string(my_string):
    s = Stack()
    # Make a stack
    for letter in my_string:
        s.push(letter)
    # Now pop each letter off, effectively reversing the string
    rev_str = ''
    for idx in range(len(my_string)):
        rev_str = rev_str + str(s.pop())
    return rev_str

rev_str = reverse_string("We will conquer COVID-19")
print(rev_str)

# Exercise 2: check if paranthesises are balanced
def is_balanced(expression):
    # E.g. "("
    paran1Open = Stack()
    # E.g. ")"
    paran1Closed = Stack()
    # E.g. "["
    paran2Open = Stack()
    # E.g. "]"
    paran2Closed = Stack()
    # E.g. "{"
    paran3Open = Stack()
    # E.g. "}"
    paran3Closed = Stack()

    for char in expression:
        if char == "(":
            paran1Open.push(char)
        elif char == ")":
            paran1Closed.push(char)
        elif char == "[":
            paran2Open.push(char)
        elif char == "]":
            paran2Closed.push(char)
        elif char == "{":
            paran3Open.push(char)
        elif char == "}":
            paran3Closed.push(char)

    p1status = True if paran1Open.size() == paran1Closed.size() else False
    p2status = True if paran2Open.size() == paran2Closed.size() else False
    p3status = True if paran3Open.size() == paran3Closed.size() else False

    status = True if p1status and p2status and p3status else False
    return status


print(is_balanced("({a+b})"))
print(is_balanced("a+{b*c+(a-1)*2}"))
print(is_balanced("b+}-a()"))
print(is_balanced("))"))
print(is_balanced("))((a+b))}{"))