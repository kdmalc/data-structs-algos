#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detecting fraudulent credit card transactions"""

__author__ = "malcolkd"

from collections import namedtuple
import re
from statistics import median


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
            if not trans.phone[1] == "1"
            or trans.phone[2].isdigit()]


def late_night_transactions(transactions):
    """Return a list of transactions between 11:00 PM - 5:00 AM."""
    return [trans for trans in transactions
            if trans.time[0:1] > "23" or trans.time[0:1] < "05"]


def highest_transactions(transactions, n_highest=10):
    """Return a list of the n highest transactions."""
    high_trans = sorted(transactions, key=lambda x: x.amount, reverse=True)
    # high_trans.sort()
    high_n_trans = high_trans[0:n_highest]
    return high_n_trans


def median_expense(transactions):
    """Return the median value of transaction amounts."""
    amounts_list = [trans.amount for trans in transactions]
    return median(amounts_list)


def significant_transactions(transactions, n_trailing=10):
    """Return a list of significant transactions.

    A transaction is significant if the amount is greater than or equal to
    five times of the median spending for a trailing number of transactions
    """
    for idx, trans in enumerate(transactions):
        sig_trans = []
        if idx == 0:
            continue
        elif idx < n_trailing:
            start_idx = 0
        else:
            start_idx = idx-n_trailing

        trailing_trans = [trans.amount for trans in
                          transactions[start_idx:idx]]
        trailing_median = median(trailing_trans)
        if trans.amount > 5*trailing_median:
            sig_trans.append(trans)
        return sig_trans


def fraudulent_transactions(transactions):
    """Return a list of potential fraudulent transactions.

    A transaction is potentially fraudulent if all is true:
        - it is a foreign transaction
        - it happens during late night (11 PM - 5 AM)
        - it is among the top 10 highest transactions
        - significant (using 10 trailing transactions)
    """
    ft = foreign_transactions(transactions)
    lnt = late_night_transactions(transactions)
    ht = highest_transactions(transactions, n_highest=10)
    st = significant_transactions(transactions, n_trailing=10)
    return [trans for trans in transactions
            if trans in ft
            and trans in lnt
            and trans in ht
            and trans in st]


def load_transactions(filename):
    """
    Load credit card transactions from 'filename'.

    Return a list of Transaction objects
    """
    my_transactions = []
    with open("transactions.txt", 'r') as f:
        split_pattern = re.compile(r"\|")
        time_pattern = re.compile(r"\d{2}:\d{2}:\d{2}")

        for line in f.readlines():
            my_list = split_pattern.split(line)

            my_time = time_pattern.findall(line)[0]
            my_amount = float("".join([dig for dig in my_list[1]
                                       if (dig.isdigit() or dig == ".")]))
            my_company = my_list[2].strip()
            my_phone = my_list[3].strip().replace("\n", "")

            my_transactions.append(Transaction(
                my_time, my_amount, my_company, my_phone))
    return my_transactions


if __name__ == "__main__":
    transactions = load_transactions("transactions.txt")

    print("Foreign Transactions:")
    print(foreign_transactions(transactions))
    print(" ")
    print(" ")
    print(" ")
    print("Late Night Transactions:")
    print(late_night_transactions(transactions))
    print(" ")
    print(" ")
    print(" ")
    print("Highest Transactions:")
    print(highest_transactions(transactions))
    print(" ")
    print(" ")
    print(" ")
    print("Median Expense:")
    print(median_expense(transactions))
    print(" ")
    print(" ")
    print(" ")
    print("Significant Transactions:")
    print(significant_transactions(transactions))
    print(" ")
    print(" ")
    print(" ")
    print("Fraudulent Transactions:")
    print(fraudulent_transactions(transactions))
