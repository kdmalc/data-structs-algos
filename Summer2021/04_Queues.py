from collections import deque

q = deque()
q.appendleft(1)
q.appendleft(2)
q.appendleft(3)
q.appendleft(4)
q.appendleft(5)
q.pop()
q.pop()

# Creating a proper stack class (normally would just use deque())
class Queue:
    def __init__(self):
        self.buffer = deque()

    def enqueue(self, val):
        self.buffer.appendleft(val)

    def dequeue(self):
        return self.buffer.pop()

    def peek(self):
        return self.buffer[-1]

    def is_empty(self):
        return len(self.buffer)==0

    def size(self):
        return len(self.buffer)

pq = Queue()
pq.enqueue({
    'company': 'Wall Mart',
    'timestamp': '15 apr, 11.01 AM',
    'price': 131.10
})
pq.enqueue({
    'company': 'Wall Mart',
    'timestamp': '15 apr, 11.02 AM',
    'price': 132
})
pq.enqueue({
    'company': 'Wall Mart',
    'timestamp': '15 apr, 11.03 AM',
    'price': 135
})