#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""PizzaPy, Co. - Supply chain modeling with generators"""

__author__ = "malcolkd"

from time import time, sleep


def flour_sack(capacity=10):
    """Generate up to capacity number of "flour" strings."""
    for _ in range(capacity):
        yield "flour"


def yeast_jar(capacity=20):
    """Generate up to capacity number of "yeast" strings."""
    for _ in range(capacity):
        yield "yeast"


def salt_shaker(capacity=100):
    """Generate up to capacity number of "salt" strings."""
    for _ in range(capacity):
        yield "salt"


def water_faucet():
    """Generate unlimited number of "water" strings."""
    while True:
        yield "water"


# my_dough = dough_maker(flour_sack(6), yeast_jar(5),
# salt_shaker(7), water_faucet())
def dough_maker(flour, yeast, water, salt):
    """
    Generate as many "dough" strings as possible by consuming exactly
    one element from each of the iterator parameters.

    E.g. the functions are passed in
    """
    flour_str = iter(flour)
    yeast_str = iter(yeast)
    salt_str = iter(salt)

    while True:
        try:
            if ((next(flour_str) is None) or
                    (next(yeast_str) is None) or
                    (next(salt_str) is None)):
                break
        except StopIteration:
            break
        yield "dough"


def sauce_container(capacity=5):
    """Generate up to capacity number of "sauce" strings."""
    for _ in range(capacity):
        yield "sauce"


def cheese_grater(throughput=3):
    """
    Generate unlimited number of "cheese" strings, but not more than
    throughout (int) number of elements in one second. The generator should
    wait (sleep) to maintain this rule.
    """
    while True:
        start_time = time()
        num_cheeses = 0
        time_lst = [0] * throughput
        while num_cheeses != throughput:
            yield "cheese"
            time_lst[num_cheeses] = time()
            total_time = time_lst[num_cheeses] - start_time
            num_cheeses += 1
            if total_time > 1:
                break  # ? Idk what to do, this means you failed
        if total_time < 1:
            sleep(1 - total_time)


def pizza_preparator(dough, sauce, cheese):
    """
    Generate as many "raw_pizza" strings as possible by consuming one element
    from the dough and sauce iterators (each) and consuming five (5) elements
    form the cheese iterator.
    """
    dough_str = iter(dough)
    sauce_str = iter(sauce)
    cheese_str = iter(cheese)

    while True:
        try:
            dough_cond = next(dough_str) is not None
            sauce_cond = next(sauce_str) is not None
            for _ in range(5):
                next(cheese_str)
            cheese_cond = True
            if (dough_cond and sauce_cond and cheese_cond):
                yield "raw_pizza"
        except StopIteration:
            break


def oven(raw_pizzas, baking_time=1.0):
    """
    Generate as many "pizza" strings as possible by consuming one element
    from the raw_pizzas iterator but waiting (sleeping) baking_time number
    of seconds before producing the value.
    """
    raw_pizza_str = iter(raw_pizzas)

    while True:
        try:
            if (next(raw_pizza_str) is None):
                break
        except StopIteration:
            break
        sleep(baking_time)
        yield "pizza"


if __name__ == "__main__":
    # Baking Pizzas
    start_time = time()
    for pizza in oven(
        pizza_preparator(
            dough_maker(
                flour_sack(), yeast_jar(), salt_shaker(), water_faucet()
            ),
            sauce_container(),
            cheese_grater(),
        )
    ):
        now = time()
        print(f"{pizza} created in {now - start_time:.3f} seconds")
        start_time = now
