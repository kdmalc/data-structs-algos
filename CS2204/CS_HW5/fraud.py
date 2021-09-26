#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detecting fraudulent credit card transactions"""

__author__ = "malcolkd"

from collections import namedtuple
import re


def get_phone_numbers(text):
    phone_patterns = (
        re.compile(r"\d{3}-\d{3}-\d{4}"),
        re.compile(r"\(\d{3}\) \d{3}-\d{4}")
    )
    phone_numbers = []
    for phone_pattern in phone_patterns:
        phone_numbers += phone_pattern.findall(text)
    return phone_numbers


def get_links(text):
    pass
    re.compile(
        r'<a[^>]+href="([^"]+)'
        )


"""
2019-07-10 00:53:16 | $18.84 | Mccarty Inc | +1-656-321-9087
2019-07-10 10:45:35 | $53.19 | Miller, Tyler and Brennan | +1-133-495-8787x1129
2019-07-11 14:47:00 | $28.88 | Thomas-Ochoa | +1-127-502-6419
"""

Transaction = namedtuple("Transaction", ["time", "amount", "company", "phone"])


def foreign_transactions(transactions):
    """Return a list of foreign transactions."""
    # E.g. phone number doesn't start with +1
    return [trans for trans in transactions
            if not trans.phone[1] == "1"]


def late_night_transactions(transactions):
    """Return a list of transactions between 11:00 PM - 5:00 AM."""
    return [trans for trans in transactions
            if trans.time[0:1] > "23" or trans.time[0:1] < "05"]


def highest_transactions(transactions, n_highest=10):
    """Return a list of the n highest transactions."""
    high_trans = sorted(transactions, key=lambda x: x.amount, reverse=True)
    # high_trans.sort()
    high_n_trans = high_trans[1:n_highest]
    return high_n_trans


def median_expense(transactions):
    """Return the median value of transaction amounts."""
    pass


def significant_transactions(transactions, n_trailing=10):
    """Return a list of significant transactions.

    A transaction is significant if the amount is greater than or equal to
    five times of the median spending for a trailing number of transactions
    """
    pass


def fraudulent_transactions(transactions):
    """Return a list of potential fraudulent transactions.

    A transaction is potentially fraudulent if all is true:
        - it is a foreign transaction
        - it happens during late night (11 PM - 5 AM)
        - it is among the top 10 highest transactions
        - significant (using 10 trailing transactions)
    """
    pass


def load_transactions(filename):
    """
    Load credit card transactions from 'filename'.

    Return a list of Transaction objects
    """
    my_transactions = []
    with open("transactions_test.txt", 'r') as f:
        split_pattern = re.compile(r"\|")
        time_pattern = re.compile(r"\d{2}:\d{2}:\d{2}")
        phone_pat1 = re.compile(r'\+\d{1}-\d{3}-\d{3}-[^"]+')
        phone_pat2 = re.compile(r'\+\d{1}-\d{3}-\d{3}-[^"]+')
        phone_pat3 = re.compile(r'\+\d{2} \d{2} \d{3}-[^"]+')
        my_phone_patterns = [phone_pat1, phone_pat2, phone_pat3]
        # OTHER PHONE PATTERNS TO ACCEPT!!!
        # +1-133-495-8787x11296
        # +36 24 197-2587
        # +1-945-634-5202x407

        for line in f.readlines():
            my_list = split_pattern.split(line)

            my_time = time_pattern.findall(line)[0]
            my_amount = float("".join([dig for dig in my_list[1]
                                       if (dig.isdigit() or dig == ".")]))
            my_company = my_list[2].strip()

            my_phone = ""  # "0000"
            for p_pat in my_phone_patterns:
                my_phone = my_phone.join(p_pat.findall(line))
                if len(my_phone.join(p_pat.findall(line))) != 0:
                    my_phone = my_phone.join(p_pat.findall(line)[0])
                else:
                    print(type(my_phone.join(p_pat.findall(line))))
                """
                try:
                    my_phone.join(p_pat.findall(line)[0])
                except IndexError:
                    print("INDEX ERROR!")
                    if ((my_phone.join(p_pat.findall(line))) is not None):
                        if type(my_phone.join(p_pat.findall(line))) is not int:
                            print(my_phone.join(p_pat.findall(line)))
                        elif (len(my_phone.join(p_pat.findall(line)) != 0)):
                            try:
                                my_phone.join(p_pat.findall(line))
                            except IndexError:
                                print("INDEX ERROR 2!")
                """
            print(len(my_phone))

            my_transactions.append(Transaction(
                my_time, my_amount, my_company, my_phone))
    return my_transactions


if __name__ == "__main__":
    transactions = load_transactions("transactions_test.txt")

    print(foreign_transactions(transactions))
    print(" ")
    print(" ")
    print(" ")
    print(late_night_transactions(transactions))
    print(" ")
    print(" ")
    print(" ")
    print(highest_transactions(transactions))
    print(" ")
    print(" ")
    print(" ")
    # print(median_expense(transactions))
    # print(significant_transactions(transactions))
    # print(fraudulent_transactions(transactions))
