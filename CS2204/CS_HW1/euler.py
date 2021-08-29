#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Estimation methods for the Euler Number"""
__author__ = "malcolkd"

from math import prod


def series(n_terms=1000):
    """Estimate e with series: 1/1 + 1/1 + 1/(1*2) + 1/(1*2*3) + ..."""
    # 1 divided by the product of 1 to idx+1, all the way up to n_terms
    e = sum([1/prod(list(range(1, idx+1))) for idx in range(n_terms)])
    return e


def limit(n_limit=1000):
    """Estimate e with limit: (1 + 1/n) ^ n"""
    e = (1 + 1/n_limit) ** n_limit
    return e


if __name__ == "__main__":
    # Test cases
    print("series(10) =", series(10))
    print("limit(1000000) =", limit(1000000))
