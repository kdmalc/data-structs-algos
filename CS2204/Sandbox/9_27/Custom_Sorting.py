# -*- coding: utf-8 -*-
"""
Created on Mon Sep 27 10:26:35 2021

@author: malcolkd
"""


def bubble_sort(lst):
    # O(n^2): two nested for loops

    # Can only do n-1 comparisons since we make n-1 comparisons
    # E.g. since we compare 2 at a time, we can't go all the way to n
    for i in range(len(lst)):
        for j in range(1, len(lst)):
            if lst[j] < lst[j-1]:
                # Switch the roles
                lst[j], lst[j-1] = lst[j-1], lst[j]
    return lst


def insertion_sort(lst):
    # O(n^2): two nested for loops
    # Do the swapping inside the first loop, not the inner loop
    # This is n^2 but actually more efficient than bubble,
    # because of the reason above

    for i in range(len(lst)):
        max_pos = 0
        # Start range from 1 since we init'd max_pos to idx 0
        # E.g. assuming idx 0 is the max element so far
        for j in range(1, len(lst) - i):
            if lst[j] >= lst[max_pos]:
                max_pos = j
        lst[max_pos], lst[j] = lst[j], lst[max_pos]
    return lst


def merge_sort(lst):
    # This is how Python actually does it
    if len(lst) <= 1:
        return lst

    mid = len(lst) // 2
    left = merge_sort(lst[:mid])
    right = merge_sort(lst[mid:])

    # E.g. keep merging until we're ready to start comparing and merging
    result = []
    i, j, = 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1  # E.g. shift the pointer on the left hand side
        else:
            result.append(right[j])
            j += 1
    # Add this in case all the smaller values are on one side and we
    # exhaust that side before even getting to the other side
    result += left[i:]
    result += right[j:]
    return result


if __name__ == "__main__":
    from random import sample

    i = 0
    for algorithm in (bubble_sort, insertion_sort, merge_sort, sorted):
        print(i)
        ordered = list(range(100))
        # Puts list in a random order since we are sampling the whole list
        unordered = sample(ordered, len(ordered))

        res = algorithm(unordered)
        assert res == ordered
        i += 1
