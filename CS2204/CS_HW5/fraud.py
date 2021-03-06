#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Detecting fraudulent credit card transactions"""

__author__ = "malcolkd"

from collections import namedtuple
import re
from statistics import median


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
            if trans.time.split()[1][0:2] >= "23"
            or trans.time.split()[1][0:2] < "05"]


def highest_transactions(transactions, n_highest=10):
    """Return a list of the n highest transactions."""
    high_trans = sorted(transactions, key=lambda x: x.amount, reverse=True)
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
    sig_trans = []
    for idx, trans in enumerate(transactions):
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
    with open(filename, 'r', encoding='utf-8') as f:
        split_pattern = re.compile(r"\|")

        for line in f.readlines():
            my_list = split_pattern.split(line)

            my_time = my_list[0].strip()
            my_amount = float("".join([dig for dig in my_list[1]
                                       if (dig.isdigit() or dig == ".")]))
            my_company = my_list[2].strip()
            my_phone = my_list[3].strip().replace("\n", "")

            my_transactions.append(Transaction(
                my_time, my_amount, my_company, my_phone))
    return my_transactions


if __name__ == "__main__":
    transactions = load_transactions("transactions.txt")

    print(f"Foreign Transactions: {len(foreign_transactions(transactions))}")
    print(foreign_transactions(transactions))
    print(" ")
    print(" ")
    print(" ")
    lnt = (late_night_transactions(transactions))
    print(f"Late Night Transactions: {len(lnt)}")
    print(lnt[0:15])
    print(" ")
    print(" ")
    print(" ")
    print(f"Highest Transactions: {len(highest_transactions(transactions))}")
    print(highest_transactions(transactions))
    print(" ")
    print(" ")
    print(" ")
    print(f"Median Expense: {(median_expense(transactions))}")
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
