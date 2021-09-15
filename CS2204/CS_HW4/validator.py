#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validator script for CS 2204 Homework submissions"""
import sys
import os
import traceback
from contextlib import redirect_stdout, redirect_stderr
from importlib.util import spec_from_file_location, module_from_spec
from io import StringIO
from math import isclose

import pycodestyle


#########################################################################
# Test infrastructure


def points(val):
    """Simple decorator to add a __points__ property to a function
    Usage: @points(10)
    """

    def decorator(func):
        func.__points__ = val
        return func

    return decorator


def abort(func):
    """Simple decorator to add a __abort__ property to a function"""
    func.__abort__ = True
    return func


def import_file(filename, module_name=None):
    """Import a file with a given module name. Returns the module object"""
    if module_name is None:
        module_name, _ = os.path.splitext(os.path.basename(filename))
    spec = spec_from_file_location(module_name, filename)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def run_file(filename):
    """Runs the file at the top-level. Returns standard output, error tuple"""
    with StringIO() as stdout, StringIO() as stderr:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            import_file(filename, "__main__")
            out = stdout.getvalue()
            err = stderr.getvalue()

    return out, err


def check_pep8_style(filename):
    """Checking PEP8 style for filename. Returns n_errors, messages tuple"""

    with StringIO() as out, redirect_stdout(out), redirect_stderr(sys.stdout):

        pep8_checker = pycodestyle.Checker(filename, show_source=True)
        pep8_errors = pep8_checker.check_all()
        pep8_msgs = out.getvalue()

    return pep8_errors, pep8_msgs


def validate(*tests):
    """Validation function"""
    total_score = 0
    divider = "-" * 45

    for test in tests:
        max_points = getattr(test, "__points__", 0)
        abort = False

        print(divider)
        prefix = f"{test.__doc__}:"
        print(f"{prefix:<{len(divider) - 10}}", end="")
        try:
            with StringIO() as out, redirect_stdout(out), redirect_stderr(
                sys.stdout
            ):

                partial = test()
                msg = out.getvalue()

        except:  # noqa
            with StringIO() as tb_out:
                traceback.print_exc(limit=-1, file=tb_out)
                msg = tb_out.getvalue()

            points = min(max_points, 0)
            abort = getattr(test, "__abort__", False)

        else:
            if partial is not None:
                points = partial
                if partial == 0:
                    abort = getattr(test, "__abort__", False)
            else:
                points = max(max_points, 0)

        suffix = "ok"
        if max_points <= 0:
            if points != 0:
                suffix = f"{points:+d} pts"
        else:
            suffix = f"{points}/{max_points} pts"
        print(f"{suffix:>10}")

        if msg:
            print(f"\n\n{msg}")

        total_score += points

        if abort:
            print("Aborting future tests. Fix this one, first!")
            break

    total_score = max(total_score, 0)
    print("=" * len(divider))
    print(f"Final score (estimated): {total_score:.0f} pts")


#########################################################################
# Assignment-specific tests

# Notes:
# You can set the max positive points for each test with @points()
# You can also set a negative value with @points, it is interpreted as penalty.
# If the test returns with
#  - None: max positive points are added, no penalties are applied
#  - Number: a given points are added, if negative, given penalties are applied
#  - Exception: no positive points are added, max penalties applied


@abort
@points(6)
def test_element():
    """Testing Element type (namedtuple)"""
    module = import_file("chemistry.py")
    if not hasattr(module, "Element"):
        print("Element data type is not defined.")
        return 0
    if not issubclass(module.Element, tuple):
        print("Element data type is not a namedtuple.")
        return 0
    for field in "number", "name", "symbol", "weight":
        if not hasattr(module.Element, field):
            print(f"Element data type does not have a '{field}' field.")
            return 0
    hydrogen = module.Element(1, "H", "Hydrogen", 1.00794)
    assert hydrogen.number == 1
    assert hydrogen.symbol == "H"
    assert hydrogen.name == "Hydrogen"
    assert isclose(hydrogen.weight, 1.00794)


@points(14)
def test_load_elements():
    """Testing load_elements"""
    module = import_file("chemistry.py")
    module.load_elements("elements.txt")
    assert isinstance(module.elements, list)
    assert len(module.elements) == 116
    assert isinstance(module.elements[0], module.Element)


@points(10)
def test_element_by_number():
    """Testing element_by_number"""
    module = import_file("chemistry.py")
    module.load_elements("elements.txt")
    assert module.element_by_number(13).name == "Aluminium"
    assert module.element_by_number(999) is None


@points(10)
def test_element_by_symbol():
    """Testing element_by_symbol"""
    module = import_file("chemistry.py")
    module.load_elements("elements.txt")
    assert module.element_by_symbol("Fe").name == "Iron"
    assert module.element_by_symbol("J") is None


@points(10)
def test_element_by_name():
    """Testing element_by_name"""
    module = import_file("chemistry.py")
    module.load_elements("elements.txt")
    assert module.element_by_name("Cobalt").symbol == "Co"
    assert module.element_by_name("Papaya") is None


@points(25)
def test_compound_elements():
    """Testing compound_elements"""
    module = import_file("chemistry.py")
    module.load_elements("elements.txt")

    salt_elements = set(module.compound_elements("NaCl"))
    assert salt_elements == set(
        [module.element_by_symbol("Na"), module.element_by_symbol("Cl")]
    )

    sucrose_elements = set(module.compound_elements("C12H22O11"))
    assert sucrose_elements == set(
        [
            module.element_by_symbol("C"),
            module.element_by_symbol("H"),
            module.element_by_symbol("O"),
        ]
    )

    silver_nitrate_elements = set(module.compound_elements("AgNO3"))
    assert silver_nitrate_elements == set(
        [
            module.element_by_symbol("Ag"),
            module.element_by_symbol("N"),
            module.element_by_symbol("O"),
        ]
    )

    ethanol_elements = set(module.compound_elements("C2H5OH"))
    assert ethanol_elements == set(
        [
            module.element_by_symbol("C"),
            module.element_by_symbol("H"),
            module.element_by_symbol("O"),
        ]
    )


@points(25)
def test_compound_weight():
    """Testing compound_weight"""
    module = import_file("chemistry.py")
    module.load_elements("elements.txt")

    assert isclose(module.compound_weight("NaCl"), 58.44277)
    assert isclose(module.compound_weight("C12H22O11"), 342.29648)
    assert isclose(module.compound_weight("AgNO3"), 169.8731)
    assert isclose(module.compound_weight("C2H5OH"), 46.068439999999995)


@points(-10)
def test_author():
    """Checking author information"""
    module = import_file("chemistry.py")
    author = getattr(module, "__author__", None)
    assert (
        isinstance(author, str) and author
    ), "__author__ variable is not set properly"


def test_pep8():
    """Checking PEP8 style"""

    n_errors, msgs = check_pep8_style("chemistry.py")
    if n_errors:
        print(msgs)
        return -n_errors


if __name__ == "__main__":
    validate(
        test_element,
        test_load_elements,
        test_element_by_number,
        test_element_by_symbol,
        test_element_by_name,
        test_compound_elements,
        test_compound_weight,
        test_author,
        test_pep8,
    )
