# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 10:36:35 2021

@author: kdmen
"""

import requests
import json
from datetime import datetime, timedelta
from pprint import pprint
import matplotlib.pyplot as plt

API_BASE = "https://api.coindesk.com/v1/bpi"


def get_current_price():
    url = f"{API_BASE}/currentprice.json"
    result = requests.get(url).text
    data = json.loads(result)

    return data["bpi"]["USD"]["rate"]


def get_history(days=30):
    end = datetime.today()
    start = end - timedelta(days=days)
    # By default, Python concatenates strings not separated by any operators
    url = (
        f"{API_BASE}/historical/close.json"
        f"?start={start:%Y-%m-%d}&end={end:%Y-%m-%d}"
        )
    # start:%Y-%m-%d
    # ^ : works the same as it does for floats, it allows you to specify how
    # to format what you entered in
    print(url)
    result = requests.get(url).text
    data = json.loads(result)
    pprint(data)
    # Let's only return the data as a list so it's easy to work with
    return [rate for rate in data["bpi"].values()]


if __name__ == "__main__":
    url = f"{API_BASE}/currentprice.json"
    result = requests.get(url).text
    # .text turns the result into a string

    # Now parse the "json" file (really it's a Python object now)
    data = json.loads(result)
    # ^json.loads is like json.load but it parses a string instead of real json
    # data object will be a dictionary
    pprint(data)
    # pprint formats the data for us

    print(f"Current Bitcoin price: ${get_current_price()}")

    days = 365
    plt.plot(get_history(days))
    plt.ylabel("USD")
    plt.xlabel("Days")
    plt.grid()
    plt.title("BTC Price Over the Last {days} Days")
