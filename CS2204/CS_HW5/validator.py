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
    """
    Simple decorator to add a __points__ property to a function.

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


@points(15)
def test_load_transactions():
    """Testing load_transactions"""
    module = import_file("fraud.py")
    transactions = module.load_transactions("transactions.txt")
    assert len(transactions) == 1000
    first_transaction = transactions[0]
    assert isinstance(first_transaction, module.Transaction)
    assert isinstance(first_transaction.amount, float)


@points(10)
def test_foreign_transactions():
    """Testing foreign_transactions"""
    module = import_file("fraud.py")
    transactions = module.load_transactions("transactions.txt")
    Transaction = module.Transaction

    expected = [
        Transaction(
            time="2019-07-13 17:02:56",
            amount=12.39,
            company="Fazekas Márton Kht.",
            phone="+36 24 197-2587",
        ),
        Transaction(
            time="2019-11-15 01:58:00",
            amount=2.53,
            company="Balog és Sándor Bt.",
            phone="+36 94 543-2730",
        ),
        Transaction(
            time="2019-12-31 07:55:39",
            amount=27.84,
            company="Kiss Kiss Nyrt.",
            phone="+36 49 013-1271",
        ),
        Transaction(
            time="2020-01-10 21:53:44",
            amount=27.62,
            company="Fazekas Márton Kht.",
            phone="+36 24 197-2587",
        ),
        Transaction(
            time="2020-09-25 05:31:19",
            amount=21.27,
            company="Farkas és Tóth Kft.",
            phone="+36 18 451-6142",
        ),
        Transaction(
            time="2020-11-25 07:01:18",
            amount=40.36,
            company="Farkas és Tóth Kft.",
            phone="+36 18 451-6142",
        ),
        Transaction(
            time="2021-03-22 03:26:15",
            amount=40.97,
            company="Kiss Kiss Nyrt.",
            phone="+36 49 013-1271",
        ),
        Transaction(
            time="2021-03-24 04:52:59",
            amount=32.43,
            company="Németh és Pataki Kkt.",
            phone="+36 40 980-1149",
        ),
        Transaction(
            time="2021-08-30 02:30:08",
            amount=150.32,
            company="Kiss Kiss Nyrt.",
            phone="+36 49 013-1271",
        ),
        Transaction(
            time="2021-12-24 16:17:35",
            amount=15.51,
            company="Farkas és társa Kft.",
            phone="+36 51 179-5649",
        ),
        Transaction(
            time="2022-01-10 14:36:17",
            amount=28.25,
            company="Horváth Kft.",
            phone="+36 59 701-8645",
        ),
    ]

    returned = module.foreign_transactions(transactions)
    assert set(expected) == set(returned)


@points(15)
def test_late_night_transactions():
    """Testing late_night_transactions"""
    module = import_file("fraud.py")
    transactions = module.load_transactions("transactions.txt")
    returned = module.late_night_transactions(transactions)
    Transaction = module.Transaction

    expected_subset = [
        Transaction(
            time="2019-10-08 01:54:52",
            amount=11.39,
            company="Boone-Perkins",
            phone="+1-608-511-7806x40298",
        ),
        Transaction(
            time="2020-07-14 02:57:21",
            amount=36.12,
            company="Blake-Mendez",
            phone="+1-719-444-6668",
        ),
        Transaction(
            time="2019-11-03 00:35:49",
            amount=36.19,
            company="Thomas Group",
            phone="+1-186-760-3400x01721",
        ),
        Transaction(
            time="2021-01-15 03:44:59",
            amount=27.45,
            company="Hayden PLC",
            phone="+1-549-237-6645x5206",
        ),
        Transaction(
            time="2020-07-09 04:01:25",
            amount=22.66,
            company="Taylor and Sons",
            phone="+1-828-897-7935x713",
        ),
    ]

    assert len(returned) == 239
    assert set(returned) > set(expected_subset)


@points(15)
def test_highest_transactions():
    """Testing highest_transactions"""
    module = import_file("fraud.py")
    transactions = module.load_transactions("transactions.txt")
    Transaction = module.Transaction

    expected_top_five = [
        Transaction(
            time="2019-11-09 19:35:55",
            amount=181.75,
            company="White-Carr",
            phone="+1-683-988-9471x923",
        ),
        Transaction(
            time="2021-08-30 02:30:08",
            amount=150.32,
            company="Kiss Kiss Nyrt.",
            phone="+36 49 013-1271",
        ),
        Transaction(
            time="2020-10-17 23:26:23",
            amount=78.2,
            company="Patel-Weeks",
            phone="+1-381-739-3537x971",
        ),
        Transaction(
            time="2019-08-21 16:19:46",
            amount=76.8,
            company="Clark, Kelley and Friedman",
            phone="+1-602-680-3985x7997",
        ),
        Transaction(
            time="2021-04-21 09:19:58",
            amount=76.73,
            company="Christensen LLC",
            phone="+1-171-332-0562",
        ),
    ]

    returned_top_five = module.highest_transactions(transactions, 5)
    assert set(returned_top_five) == set(expected_top_five)
    assert len(module.highest_transactions(transactions, 10)) == 10
    assert len(module.highest_transactions(transactions, 25)) == 25


@points(15)
def test_median_expense():
    """Testing median_expense"""
    module = import_file("fraud.py")
    transactions = module.load_transactions("transactions.txt")
    assert isclose(module.median_expense(transactions), 21.925)


@points(15)
def test_significant_transactions():
    """Testing significant_transactions"""
    module = import_file("fraud.py")
    transactions = module.load_transactions("transactions.txt")
    returned = module.late_night_transactions(transactions)
    Transaction = module.Transaction

    expected = [
        Transaction(
            time="2019-11-09 19:35:55",
            amount=181.75,
            company="White-Carr",
            phone="+1-683-988-9471x923",
        ),
        Transaction(
            time="2020-06-29 04:31:39",
            amount=47.73,
            company="Moore-Oliver",
            phone="+1-956-998-4999x4202",
        ),
        Transaction(
            time="2021-08-30 02:30:08",
            amount=150.32,
            company="Kiss Kiss Nyrt.",
            phone="+36 49 013-1271",
        ),
    ]

    returned = module.significant_transactions(transactions, 20)
    assert set(expected) == set(returned)
    assert len(module.significant_transactions(transactions, 5)) == 34
    assert len(module.significant_transactions(transactions, 10)) == 10
    assert len(module.significant_transactions(transactions, 15)) == 9


@points(15)
def test_fraudulent_transactions():
    """Testing fraudulent_transactions"""
    module = import_file("fraud.py")
    transactions = module.load_transactions("transactions.txt")
    Transaction = module.Transaction

    expected_fraudulent = [
        Transaction(
            time="2021-08-30 02:30:08",
            amount=150.32,
            company="Kiss Kiss Nyrt.",
            phone="+36 49 013-1271",
        )
    ]

    returned_fraudulent = module.fraudulent_transactions(transactions)
    assert set(expected_fraudulent) == set(returned_fraudulent)


@points(-10)
def test_author():
    """Checking author information"""
    module = import_file("fraud.py")
    author = getattr(module, "__author__", None)
    assert (
        isinstance(author, str) and author
    ), "__author__ variable is not set properly"


def test_pep8():
    """Checking PEP8 style"""

    n_errors, msgs = check_pep8_style("fraud.py")
    if n_errors:
        print(msgs)
        return -n_errors


if __name__ == "__main__":
    validate(
        test_load_transactions,
        test_foreign_transactions,
        test_late_night_transactions,
        test_highest_transactions,
        test_median_expense,
        test_significant_transactions,
        test_fraudulent_transactions,
        test_author,
        test_pep8,
    )
