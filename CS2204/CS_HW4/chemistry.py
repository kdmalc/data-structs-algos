#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chemical elements and compunds"""

__author__ = "malcolkd"

from collections import namedtuple

# TODO: define the Element datatype (using namedtuple)
# Element = ...

elements = []


def load_elements(filename):
    """Load text database of chemical elements to initialize the module.

    Add the Element objects to the global elements list"""
    with open(filename) as db:
        for line in db:
            # line is a single string of from the file
            pass


def element_by_number(number):
    """Return the chemical element of a given atomic number

    Return None if element is not found.
    """
    pass


def element_by_symbol(symbol):
    """Return the chemical element of a given symbol

    Return None if element is not found.
    """
    pass


def element_by_name(name):
    """Return the chemical element of a given name.

    Name matching is case-insensitive.
    Return None if element is not found.
    """
    pass


def compound_elements(formula):
    """Return the list of elements in a given compound formula."""
    pass


def compound_weight(formula):
    """Return the total weight of a given compound formula."""
    pass


if __name__ == "__main__":
    load_elements("elements.txt")

    # Feel free to use (umcomment) these examples to try out your code

    # print("The 17. element:", element_by_number(17).name)
    # print("The name of Ge:", element_by_symbol("Ge").name)
    # print("The weight of Oxygen:", element_by_name("Oxygen").weight)

    # print("The elements in salt:", compound_elements("NaCl"))
    # print("The molecular weight of Caffeine", compound_weight("C8H10N4O2"))
