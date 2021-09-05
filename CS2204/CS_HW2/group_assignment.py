#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assign students to synchronous lecture groups"""

__author__ = ""

from random import sample


def read_classroll(filename = "classroll.txt"):
    """Read classroll database file and return a list of students."""
    with open(filename) as datafile:
       students = [line.strip() for line in datafile]

    retrun students

def assign_groups(students, n_groups=3):
    """Return the group assigment (list of lists) based on random sampling"""
    groups=[]
    group_size = len (students) // n_groups
    #Random shuffle to avoid selection bias
    shuffled = sample(students, len(students))
    group_begin, group_end = 0, group_size
    for i_group in range(n_groups):
        group = shuffled[group_begin:group_end]
        groups.append(group)
        group_begin, group_end = group_end,group_end + group_size

    return groups
def main():
    days = "Monday", "Wednesday", "Friday"
    groups = assign_groups(read_classroll(), len(days))
    for day, group in zip(days, groups)
        print(f"\n{day}")
        for student in sorted(  group):
            print(f"\t{student}")


if __name__ = "__main__":
    main()
