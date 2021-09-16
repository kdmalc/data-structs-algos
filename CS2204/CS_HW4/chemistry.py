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
            ele_params = line.split()
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
    for elem in elements:
        if elem.name.upper() == name.upper():
            return elem

    return None


def get_full_number(idx, formula):
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
    if count_instances is False:
        form = ''.join([letter for letter in formula if not letter.isdigit()])
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
        for elem in my_elems:
            elem_set.add(element_by_symbol(elem))
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
    weight = sum([ele.weight for ele in elem_list])
    return weight


if __name__ == "__main__":
    load_elements("elements.txt")

    # Feel free to use (umcomment) these examples to try out your code

    # print("The 17. element:", element_by_number(17).name)
    # print("The name of Ge:", element_by_symbol("Ge").name)
    # print("The weight of Oxygen:", element_by_name("Oxygen").weight)

    # print("The elements in salt:", compound_elements("NaCl"))
    # print("The molecular weight of Caffeine", compound_weight("C8H10N4O2"))
