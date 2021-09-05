#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validator script for CS 2204 Homework submissions"""
import sys
import os
import traceback
from contextlib import redirect_stdout, redirect_stderr
from importlib.util import spec_from_file_location, module_from_spec
from io import StringIO

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


def almost_equal(a, b, places=7):
    """Compare if to floats are almost equal"""
    return round(abs(a - b), places) == 0


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

    with StringIO() as out, \
            redirect_stdout(out), \
            redirect_stderr(sys.stdout):

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
            with StringIO() as out, \
                    redirect_stdout(out), \
                    redirect_stderr(sys.stdout):

                partial = test()
                msg = out.getvalue()

        except:     # noqa
            with StringIO() as tb_out:
                traceback.print_exc(limit=-1, file=tb_out)
                msg = tb_out.getvalue()

            points = min(max_points, 0)
            abort = getattr(test, "__abort__", False)

        else:
            if partial is not None:
                points = partial
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


@points(30)
@abort
def test_syntax():
    """Testing syntax errors"""
    run_file("group_assignment.py")


def parse_output(output):
    """Utility function to parse the assignment output text.

    Returns a dictionary of lists {day: students}. May raise exceptions.
    """
    import string
    assignments = {}
    day = None
    valid_days = {"Monday", "Wednesday", "Friday"}
    for line in output.splitlines():
        if not line.strip():
            continue
        if line[0] in string.whitespace:
            student = line.strip()
            assert len(student.split()) == 2, f"Invalid name: {student}"
            assert day is not None, f"Student name(s) without day: {student}"
            assignments.setdefault(day, []).append(student)
        else:
            day = line.strip()
            assert day in valid_days, f"Invalid day: {day}"
            assert day not in assignments, f"Duplicated day: {day}"
    return assignments


@points(20)
def test_output_format():
    """Testing output format"""
    out, err = run_file("group_assignment.py")
    parse_output(out)


@points(50)
def test_correct_assignment():
    """Testing correct assigment"""
    out, err = run_file("group_assignment.py")
    assignments = parse_output(out)
    if len(assignments) != 3:
        print(f"Not all days are used: {tuple(assignments.keys())}")
        return 0
    assigned_students = set()
    min_assignment, max_assignment = sys.maxsize, 0
    for students in assignments.values():
        min_assignment = min(min_assignment, len(students))
        max_assignment = max(max_assignment, len(students))
        for student in students:
            if student in assigned_students:
                print(f"Student: {student} assigned multiple times")
                return 0
            assigned_students.add(student)

    if abs(max_assignment - min_assignment) > 1:
        print("Unbalanced days (group sizes differ by more than one student")
        return 0

    with open("classroll.txt") as classroll:
        if len(classroll.readlines()) != len(assigned_students):
            print("Not all students are assigned")
            return 0


@points(-10)
def test_author():
    """Checking author information"""
    module = import_file("group_assignment.py")
    author = getattr(module, "__author__", None)
    assert isinstance(author, str) and author, \
        "__author__ variable is not set properly"


def test_pep8():
    """Checking PEP8 style"""

    n_errors, msgs = check_pep8_style("group_assignment.py")
    if n_errors:
        print(msgs)
        return -n_errors


if __name__ == "__main__":
    validate(
        test_syntax,
        test_output_format,
        test_correct_assignment,
        test_author,
        test_pep8,
    )
