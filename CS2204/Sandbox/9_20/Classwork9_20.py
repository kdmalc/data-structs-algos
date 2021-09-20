# -*- coding: utf-8 -*-
"""
Created on Mon Sep 20 10:46:40 2021

@author: kdmen
"""

import urllib
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
    link_pattern = re.compile(
        r'<a[^>]+href="([^"]+)'
        )
    # ^ is a not symbol
    # "Anything else except for a closing bracket"
    return link_pattern.findall(text)


def crawl(start_url, max_pages=15):
    todo = [start_url]
    n_pages = 0
    while todo and n_pages < max_pages:
        url = todo.pop(0)
        try:
            data = urllib.request.urlopen(url).read()
        except Exception:
            continue  # E.g. skip this file since it won't open
        text = str(data)
        for phone_number in get_phone_numbers(text):
            print(phone_number)

        for link in get_links(text):
            todo.append(link)

        n_pages += 1


if __name__ == "__main__":
    url = "https://www.vanderbilt.edu"
    crawl(url)
