#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Chemical elements and compunds"""

__author__ = "malcolkd"

from collections import namedtuple

# TODO: define the Element datatype (using namedtuple)
Element = namedtuple("Element", ["number", "symbol", "name", "weight"])

elements = []


def load_elements(filename):
    """Load text database of chemical elements to initialize the module.

    Add the Element objects to the global elements list"""
    with open(filename) as db:
        for line in db:
            # line is a single string of from the file
            ele_params = line.strip().split()
            elements.append(Element(int(ele_params[0]), ele_params[1],
                                    ele_params[2], float(ele_params[3])))


def element_by_number(num):
    """Return the chemical element of a given atomic number

    Return None if element is not found.
    """
    for elem in elements:
        if elem.number == num:
            return elem

    return None


def element_by_symbol(sym):
    """Return the chemical element of a given symbol

    Return None if element is not found.
    """
    for elem in elements:
        if elem.symbol == sym:
            return elem

    return None


def element_by_name(name):
    """Return the chemical element of a given name.

    Name matching is case-insensitive.
    Return None if element is not found.
    """
    if not type(name) is str:
        print("Please enter a string!")
        return None

    for elem in elements:
        if elem.name.upper() == name.upper():
            return elem

    return None


def get_full_number(idx, formula):
    """Return the full number (as an int) taken from a string
    E.g. if the string is "O123", this function retrieves "123"

    Returns 0 if it is detected that there is no num
    """
    num_str = ""
    while formula[idx].isdigit():
        num_str = num_str + formula[idx]
        idx += 1
        if idx == len(formula):
            break
    if num_str:
        return int(num_str)
    else:
        return 0


def compound_elements(formula, count_instances=False):
    """Return the list of elements in a given compound formula."""
    if ((type(formula) is not str) or (formula[0] == formula[0].lower())
            or (not formula)):
        print("Invalid input!")
        return None

    if count_instances is False:
        form = ''.join([letter for letter in formula
                        if not letter.isdigit()])
        # Assuming form will be: (CAP lower) (CAP) (CAP lower) (CAP)
        my_elems = []
        for char in form:
            if char.isupper():
                my_elems.append(char)
            elif char.islower():
                my_elems[-1] = str(my_elems[-1]) + str(char)
            else:
                raise "Unexpected type"
        # Assuming that these are indeed the elements
        elem_set = set()
        [elem_set.add(element_by_symbol(elem)) for elem in my_elems]
        return list(elem_set)
    else:
        my_elems = []
        for idx, char in enumerate(formula):
            char_previous = formula[idx-1] if idx > 0 else ""
            if char.isupper():
                my_elems.append(char)
            elif char.islower():
                my_elems[-1] = str(my_elems[-1]) + str(char)
            elif char.isdigit():
                if char_previous.isdigit():
                    pass
                else:
                    my_num = get_full_number(idx, formula)
                    for _ in range(my_num-1):
                        my_elems.append(my_elems[-1])
            else:
                raise "Unexpected type"
        elem_list = [element_by_symbol(ele) for ele in my_elems]
        return elem_list


def compound_weight(formula):
    """Return the total weight of a given compound formula."""
    elem_list = compound_elements(formula, count_instances=True)
    if elem_list is None:
        return None
    else:
        return sum([ele.weight for ele in elem_list])


if __name__ == "__main__":
    load_elements("elements.txt")

    # Feel free to use (umcomment) these examples to try out your code

    print("The 17. element:", element_by_number(17).name)
    print("The 123412 element: (True if invalid) ",
          element_by_number(123412) is None)
    print("The name of Ge:", element_by_symbol("Ge").name)
    print("The name of asdfasdf: (True if invalid) ",
          element_by_symbol("asdfasdf") is None)
    print("The weight of Oxygen:", element_by_name("Oxygen").weight)

    print("The elements in salt:", compound_elements("NaCl"))
    print("The elements in salt:", compound_elements("aNCl"))
    print("The elements in salt:", compound_elements("12"))
    print("The elements in salt:", compound_elements(12))
    print("The molecular weight of Caffeine", compound_weight("C8H10N4O2"))
    print("The molecular weight of Caffeine", compound_weight("c"))
    print("The molecular weight of Caffeine", compound_weight("1738"))
    print("The molecular weight of Caffeine", compound_weight(1738))
