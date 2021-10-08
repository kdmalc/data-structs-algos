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


def _test_ingredient(source, name):
    for capacity in 1, 10, 100:
        for i, ingredient in enumerate(source(capacity)):
            assert ingredient == name
            if i >= capacity:  # too much
                break
        assert i + 1 == capacity


@points(5)
def test_flour_sack():
    """Testing flour_sack"""
    module = import_file("pizza.py")
    _test_ingredient(module.flour_sack, "flour")


@points(5)
def test_yeast_jar():
    """Testing yeast_jar"""
    module = import_file("pizza.py")
    _test_ingredient(module.yeast_jar, "yeast")


@points(5)
def test_salt_shaker():
    """Testing salt_shaker"""
    module = import_file("pizza.py")
    _test_ingredient(module.salt_shaker, "salt")


@points(5)
def test_water_faucet():
    """Testing water_faucet"""
    module = import_file("pizza.py")
    faucet = module.water_faucet()
    for i in range(1000):
        assert next(faucet) == "water"


@points(10)
def test_dough_maker():
    """Testing dough_maker"""
    module = import_file("pizza.py")

    for n_flour, n_yeast, n_salt in (
        (6, 5, 7),
        (100, 2, 8),
        (1, 99, 4),
        (42, 42, 42),
    ):

        flour = module.flour_sack(n_flour)
        yeast = module.yeast_jar(n_yeast)
        salt = module.salt_shaker(n_salt)
        water = module.water_faucet()
        n_dough = min(n_flour, n_yeast, n_salt)

        for i, dough in enumerate(
            module.dough_maker(flour, yeast, salt, water)
        ):
            assert dough == "dough"
            if i >= n_dough:  # too much
                break

        assert i + 1 == n_dough
        # This is too hard: you may need to consume some to realize there is
        # not enough left
        # assert len(list(flour)) == n_flour - n_dough
        # assert len(list(yeast)) == n_yeast - n_dough
        # assert len(list(salt)) == n_salt - n_dough


@points(5)
def test_sauce_container():
    """Testing sauce_container"""
    module = import_file("pizza.py")
    _test_ingredient(module.sauce_container, "sauce")


@points(25)
def test_cheese_grater():
    """Testing cheese_grater"""
    from itertools import islice
    from time import time

    module = import_file("pizza.py")
    for n_cheese, throughput in ((5, 5), (10, 5), (6, 5)):
        t_begin = time()
        for cheese in islice(module.cheese_grater(throughput), 0, n_cheese):
            assert cheese == "cheese"
        t_end = time()
        serving_time = t_end - t_begin
        expected_serving_time = (n_cheese - 1) // throughput
        if abs(serving_time - expected_serving_time) > 0.1:  # slack
            print(
                f"Throughput not maintained for {n_cheese} cheese"
                f" at {throughput} cheese/second throughput"
                f"\nExpected time: {expected_serving_time} seconds"
                f"\nActual time: {serving_time} seconds"
            )
            return 15


@points(20)
def test_pizza_preparator():
    """Testing pizza_preparator"""
    module = import_file("pizza.py")

    for n_dough, n_sauce, n_cheese in (
        (6, 5, 7),
        (100, 2, 8),
        (20, 99, 24),
        (42, 42, 42),
    ):

        dough = module.dough_maker(
            module.flour_sack(n_dough),
            module.yeast_jar(n_dough),
            module.salt_shaker(n_dough),
            module.water_faucet(),
        )
        sauce = module.sauce_container(n_sauce)
        cheese = iter(["cheese"] * n_cheese)  # fake it: speed-up

        n_raw_pizza = min(n_dough, n_sauce, n_cheese // 5)
        for i, raw_pizza in enumerate(
            module.pizza_preparator(dough, sauce, cheese)
        ):
            assert raw_pizza == "raw_pizza"
            if i >= n_raw_pizza:  # too much
                break

        assert i + 1 == n_raw_pizza
        # This is too hard: you may need to consume some to realize there is
        # not enough left
        # assert len(list(dough)) == n_dough - n_raw_pizza
        # assert len(list(sauce)) == n_sauce - n_raw_pizza
        # assert len(list(cheese)) == n_cheese - 5 * n_raw_pizza


@points(20)
def test_oven():
    """Testing oven"""
    from time import time

    module = import_file("pizza.py")

    for n_raw_pizzas, baking_time in ((2, 0.5), (6, 0.2), (1, 0.7)):
        # fake it: speed-up & test consumption
        raw_pizzas = iter(["raw_pizza"] * n_raw_pizzas)
        t_begin = time()
        for i, pizza in enumerate(module.oven(raw_pizzas, baking_time)):
            assert pizza == "pizza"
            if i > n_raw_pizzas:  # too much
                break
        t_end = time()

        assert i + 1 == n_raw_pizzas

        expected_time = n_raw_pizzas * baking_time
        actual_time = t_end - t_begin
        assert abs(expected_time - actual_time) < 0.1  # slack


@points(-10)
def test_author():
    """Checking author information"""
    module = import_file("pizza.py")
    author = getattr(module, "__author__", None)
    assert (
        isinstance(author, str) and author
    ), "__author__ variable is not set properly"


def test_pep8():
    """Checking PEP8 style"""

    n_errors, msgs = check_pep8_style("pizza.py")
    if n_errors:
        print(msgs)
        return -n_errors


if __name__ == "__main__":
    validate(
        test_flour_sack,
        test_yeast_jar,
        test_salt_shaker,
        test_water_faucet,
        test_dough_maker,
        test_sauce_container,
        test_cheese_grater,
        test_pizza_preparator,
        test_oven,
        test_author,
        test_pep8,
    )
