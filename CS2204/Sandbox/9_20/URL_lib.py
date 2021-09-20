# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 10:30:20 2021

@author: kdmen
"""

import urllib


r = urllib.request.urlopen("https://www.vanderbilt.edu").read()
s = str(r)  # converting byte to string

# How to find phone numbers within this string?
# Trivial example
ps = "My phone number is (555)-123-4567"

# Use regular expresions
import re

print(re.findall("555", ps))
print(re.findall("777", ps))

print(re.findall("5+", ps))
# * means zero or more appearances
# + means at least once

print(re.findall(r"\d+", ps))
# Find any digits that happen once or more
# Must make it a raw string so Python doesn't try and read the escape key
# Note that \d is not equivalent to escape in regex, rather specifies digits

print(re.findall(r"\(\d{3}\)", ps))
print(re.findall(r"\(\d{3}\)-\d{3}-\d{4}", ps))
