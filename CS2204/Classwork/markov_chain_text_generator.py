# -*- coding: utf-8 -*-
"""
Created on Mon Oct  4 10:27:38 2021

@author: kdmen
"""

# Markov Chain Text Generator
# Want to do an NLP task that writes convincing text
# Tries to mimic the grammatical rules of the English language

# Grammar creates redudnacy in the language

# Can improve using more than just 2 last words
# Worked better with Trump tweets

import requests
from random import choice

response = requests.get("https://www.gutenberg.org/files/1661/1661-0.txt")
# ^repsonse.content is of type bytes
words = response.content.decode("utf-8").split()
# ^e.g. returns a list of words
print(words[:5])

# LEARNING PHASE
next_word = {}
for i in range(2, len(words)):
    # Don't have a for loop over the words, because we consider 3 words:
    # We consider the previous two and the next one
    last_words = words[i-2], words[i-1]
    # next_word[last_words].append(words[i])
    # ^Assumes the key already exists
    next_word.setdefault(last_words, []).append(words[i])

# GENERATION
# Starting point: need 2 words
words = ["Sherlock", "Holmes"]

while len(words) < 100:
    last_words = tuple(words[-2:])
    # Must convert to a tuple in order to use as a key in the dictionary
    if last_words not in next_word:
        # Ended up in a deadend
        break
    else:
        words.append(choice(next_word[last_words]))

print(" ".join(words))
