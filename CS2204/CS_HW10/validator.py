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


@points(50)
def test_distance():
    """Testing distance()"""
    module = import_file("gps_tracking.py")

    # for _ in range(20):
    # lat1 = round(360 * random() - 180, 4)
    # lon1 = round(360 * random() - 180, 4)
    # lat2 = round(lat1 + gauss(0, 0.01), 4)
    # lon2 = round(lon1 + gauss(0, 0.01), 4)
    # print(f"(({lat1}, {lon1}),"
    #       f" ({lat2}, {lon2}),"
    #       f" {distance((lat1, lon1), (lat2, lon2))}),")
    test_vectors = (
        ((103.4608, -90.667), (103.4847, -90.6701), 1.652102706884582),
        ((48.95, 36.1026), (48.9624, 36.1038), 0.8584948477761204),
        ((12.7528, 71.7861), (12.7552, 71.7828), 0.277404395496461),
        ((165.5824, 41.2072), (165.5887, 41.2164), 0.7539967577824119),
        ((131.1756, -4.9246), (131.1681, -4.9134), 0.7266839594778721),
        ((91.8259, -49.0991), (91.8235, -49.1039), 0.1661617445452732),
        ((-134.7105, 69.9333), (-134.7322, 69.9483), 1.6672961272937856),
        ((-3.609, 13.2423), (-3.6142, 13.2415), 0.3634996930932445),
        ((78.811, 83.6586), (78.8087, 83.6714), 0.23390631753451535),
        ((77.3376, 113.489), (77.3393, 113.4729), 0.2706489081574273),
        ((-163.9515, -177.2728), (-163.9575, -177.2736), 0.41795420198316435),
        ((-7.3628, 129.3005), (-7.3516, 129.2905), 1.033644412607839),
        ((81.476, 141.5569), (81.4755, 141.541), 0.16646693681501645),
        ((73.1097, 147.6071), (73.1094, 147.6116), 0.09268413480425859),
        ((-45.8043, -171.2124), (-45.8161, -171.2175), 0.8515051757510127),
        ((119.1302, -6.3639), (119.122, -6.3606), 0.5773387052395506),
        ((171.8242, -8.2978), (171.8281, -8.2884), 0.6970764124545047),
        ((-72.9012, -161.491), (-72.9342, -161.4882), 2.2808132026488437),
        ((113.4665, -37.0892), (113.4874, -37.0915), 1.4454536710498236),
        ((-58.2663, -100.3726), (-58.2768, -100.372), 0.7258155000331443),
    )

    for p1, p2, d in test_vectors:
        assert isclose(module.distance(p1, p2), d, rel_tol=1e-3)


@points(50)
def test_output():
    """Testing the printed output"""

    out, err = run_file("gps_tracking.py")
    exp = ("Distance: 19.1 miles\n"
           "Average speed: 52 mph\n"
           "Maximum speed: 84 mph")
    if out.strip() != exp:
        print(f"\nExpected output:\n{exp}\n\nActual output:\n{out}")
        return 0


@points(-10)
def test_author():
    """Checking author information"""
    module = import_file("gps_tracking.py")
    author = getattr(module, "__author__", None)
    assert isinstance(author, str) and author, \
        "__author__ variable is not set properly"


def test_pep8():
    """Checking PEP8 style"""

    n_errors, msgs = check_pep8_style("gps_tracking.py")
    if n_errors:
        print(msgs)
        return -n_errors


if __name__ == "__main__":
    validate(
        test_distance,
        test_output,
        test_author,
        test_pep8,
    )
