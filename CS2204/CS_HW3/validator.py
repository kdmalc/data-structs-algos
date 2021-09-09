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


@points(10)
def test_codon_constructor():
    """Testing Codon class initializer"""
    module = import_file("dna.py")
    Codon = module.Codon

    # valid patterns
    for pattern in "act", "Act", "CTG":
        _ = Codon(pattern)

    # invalid patterns
    for pattern in None, 7, "", "actg", "acx":
        try:
            _ = Codon(pattern)
        except:     # noqa
            pass
        else:
            print(f"Initializer should refuse this parameter: {pattern!r}")
            return 0


@points(10)
def test_codon_str():
    """Testing Codon string conversion"""
    module = import_file("dna.py")
    Codon = module.Codon
    assert str(Codon("ACT")) == "[ACT]"
    assert str(Codon("act")) == "[ACT]"
    assert str(Codon("ggG")) == "[GGG]"


@points(10)
def test_codon_eq():
    """Testing Codon equality"""
    module = import_file("dna.py")
    Codon = module.Codon
    assert Codon("ACT") == Codon("ACT")
    assert Codon("ACT") == Codon("act")
    assert Codon("act") != Codon("acg")


@points(10)
def test_codon_transcribe():
    """Testing Codon transcription"""
    module = import_file("dna.py")
    Codon = module.Codon
    assert Codon("ACT").transcribe() == "<ACU>"
    assert Codon("act").transcribe() == "<ACU>"
    assert Codon("acg").transcribe() == "<ACG>"


@points(10)
def test_gene_constructor():
    """Testing Gene class initializer"""
    module = import_file("dna.py")
    Gene = module.Gene

    # valid patterns
    for pattern in "", "ac", "actg", "actgg", "actggc":
        _ = Gene(pattern)

    # invalid patterns
    for pattern in None, 7, "xkcd":
        try:
            _ = Gene(pattern)
        except:     # noqa
            pass
        else:
            print(f"Initializer should refuse this parameter: {pattern!r}")
            return 0


@points(10)
def test_gene_str():
    """Testing Gene string conversion"""
    module = import_file("dna.py")
    Gene = module.Gene
    assert str(Gene("")) == ""
    assert str(Gene("ac")) == ""
    assert str(Gene("act")) == "[ACT]"
    assert str(Gene("actgg")) == "[ACT]"
    assert str(Gene("actggc")) == "[ACT][GGC]"
    assert str(Gene("actggctt")) == "[ACT][GGC]"


@points(10)
def test_gene_transcribe():
    """Testing Gene transcription"""
    module = import_file("dna.py")
    Gene = module.Gene
    assert Gene("").transcribe() == ""
    assert Gene("ac").transcribe() == ""
    assert Gene("act").transcribe() == "<ACU>"
    assert Gene("actgg").transcribe() == "<ACU>"
    assert Gene("actggctt").transcribe() == "<ACU><GGC>"


@points(15)
def test_gene_contains():
    """Testing Codon search in Gene"""
    module = import_file("dna.py")
    Codon, Gene = module.Codon, module.Gene
    gene = Gene("actgggctgacctgttaaactgtc")
    assert Codon("act") in gene
    assert Codon("ggg") in gene
    assert Codon("gtt") not in gene
    assert Codon("ccc") not in gene
    assert Codon("acg") not in gene


@points(15)
def test_gc_content():
    """Testing GC content calculation"""
    from math import isclose
    from random import choices
    module = import_file("dna.py")
    Gene = module.Gene
    for k in 10, 100, 1000:
        gene_str = "".join(choices("actg", k=k))
        gene_str_cut = gene_str[:k - (k % 3)]
        gc_cnt = gene_str_cut.count("g") + gene_str_cut.count("c")
        gc_content = gc_cnt / len(gene_str_cut)
        if not isclose(gc_content, Gene(gene_str).gc_content()):
            print(f"GC content should be {gc_content} for: \n{gene_str}")
            return 0


@points(-10)
def test_author():
    """Checking author information"""
    module = import_file("dna.py")
    author = getattr(module, "__author__", None)
    assert isinstance(author, str) and author, \
        "__author__ variable is not set properly"


def test_pep8():
    """Checking PEP8 style"""

    n_errors, msgs = check_pep8_style("dna.py")
    if n_errors:
        print(msgs)
        return -n_errors


if __name__ == "__main__":
    validate(
        test_codon_constructor,
        test_codon_str,
        test_codon_eq,
        test_codon_transcribe,
        test_gene_constructor,
        test_gene_str,
        test_gene_transcribe,
        test_gene_contains,
        test_gc_content,
        test_author,
        test_pep8,
    )
