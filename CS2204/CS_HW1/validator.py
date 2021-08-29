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

DIVIDER = "-" * 45


def test_series(module):
    """Testing the series function"""
    series = module.series
    assert almost_equal(series(1), 1.0)
    assert almost_equal(series(10), 2.7182815255731922)
    assert almost_equal(series(100), 2.7182818284590455)

    return 40


def test_limit(module):
    """Testing the limit function"""
    limit = module.limit
    assert almost_equal(limit(1), 2.0)
    assert almost_equal(limit(1000), 2.7169239322355936)
    assert almost_equal(limit(1_000_000), 2.7182804690957534)

    return 40


def test_output(stdout):
    """Testing the printed output"""

    exp = ("series(10) = 2.7182815255731922\n"
           "limit(1000000) = 2.7182804690957534")
    if stdout.strip() != exp:
        assert False, f"\nExpected output:\n{exp}\n\nActual output:\n{stdout}"

    return 20


def almost_equal(a, b, places=7):
    """Compare if to floats are almost equal"""
    return round(abs(a - b), places) == 0


def print_exception(exc=None):
    print(DIVIDER)
    if exc is None:
        traceback.print_exc(limit=-1, file=sys.stdout)
    else:
        print(exc)
    print(DIVIDER)


def import_file(filename, module_name=None):
    """Import a file with a given module name. Returns the module object"""
    if module_name is None:
        module_name, _ = os.path.splitext(os.path.basename(filename))
    spec = spec_from_file_location(module_name, filename)
    module = module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def scoring():
    """Validation function"""
    total_score = 0

    filename = "euler.py"

    # validate normal import
    try:
        import_stdout, import_stderr = StringIO(), StringIO()
        with redirect_stdout(import_stdout), redirect_stderr(import_stderr):
            module = import_file(filename)
        # print(import_stderr.getvalue(), end="")
        # print(import_stdout.getvalue(), end="")
    except:         # noqa
        print(f"CRITICAL ERROR in {filename}, fix this first:")
        print_exception()
        return total_score

    # validate functions
    for test in test_series, test_limit:
        try:
            print(f"{test.__doc__}...", end="")
            score = test(module)
            print(f"PASSED: {score} pts")
            total_score += score
        except:     # noqa
            print("FAILED: 0 pts")
            print_exception()

    # validate output
    try:
        run_stdout, run_stderr = StringIO(), StringIO()
        with redirect_stdout(run_stdout), redirect_stderr(run_stderr):
            import_file(filename, "__main__")
        # print(run_stderr.getvalue(), end="")
        # print(run_stdout.getvalue(), end="")
        test = test_output
        print(f"{test.__doc__}...", end="")
        score = test(run_stdout.getvalue())
        print(f"PASSED: {score} pts")
        total_score += score
    except Exception as exc:
        print("FAILED: 0 pts")
        print_exception(exc)

    # Penalties...

    # validate author
    author = getattr(module, "__author__", None)
    if not isinstance(author, str) or not author:
        penalty = min(10, total_score)
        print(f"Author is not set: -{penalty} pts")
        total_score -= penalty

    # validate silent output
    if import_stdout.getvalue() or import_stderr.getvalue():
        penalty = min(10, total_score)
        print(f"Import is not silent (__name__ idiom): -{penalty} pts")
        total_score -= penalty

    # validate style
    pep8_stdout, pep8_stderr = StringIO(), StringIO()
    with redirect_stdout(pep8_stdout), redirect_stderr(pep8_stderr):
        pep8_checker = pycodestyle.Checker(filename, show_source=True)
        pep8_errors = pep8_checker.check_all()

    if pep8_errors:
        penalty = min(pep8_errors, total_score)
        print(f"PEP 8 style penalties: -{penalty} pts")
        print(DIVIDER)
        print(pep8_stdout.getvalue())
        print(DIVIDER)
        total_score -= penalty

    return total_score


if __name__ == "__main__":
    score = scoring()
    print("=" * len(DIVIDER))
    print(f"Final score (estimated): {score:.0f} pts")
