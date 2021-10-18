#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Checking balanced brackets"""

__author__ = "malcolkd"

from collections import deque


def is_balanced(expr):
    """Return True, if the brackets are balanced in expr, otherwise False"""

    brackets_list = ["[", "]", "{", "}", "(", ")"]
    opening_brac = ["[", "{", "("]
    closing_brac = ["]", "}", ")"]
    brac_expr = ""
    _ = [(brac_expr + char) for char in expr if (char in brackets_list)]

    meta_stack = deque()
    for char in expr:
        if char in opening_brac:
            meta_stack.append(char)
        elif char in closing_brac:
            try:
                temp = meta_stack.pop()
            except IndexError:
                print("Attempted to pop from an empty deque")
                return False
            try:
                assert opening_brac.index(temp) == closing_brac.index(char)
            except AssertionError:
                print(f"Popped {temp} does not equal current {char}")
                return False
    return True


if __name__ == "__main__":
    assert is_balanced("{[()]}") is True
    assert is_balanced("{hello[(world])}") is False
    assert is_balanced("{{[hello[(world())]]}}") is True
    assert is_balanced("({X}(A[++][--])A)[hello](world)") is True
    assert is_balanced("{)[](}]}]}))}(())(") is False
