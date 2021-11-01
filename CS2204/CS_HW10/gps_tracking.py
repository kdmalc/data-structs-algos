#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Processing GPS tracking log files"""

__author__ = "malcolkd"

import csv
from numpy import sin, cos, arctan, sqrt


# Global constants
R = 3958.8  # miles
rads = 0.01745329  # rads / deg


def haverside(p1, p2):
    phi1, phi2 = p1[0]*rads, p2[0]*rads
    lamda1, lamda2 = p1[1]*rads, p2[1]*rads

    dphi = phi2 - phi1
    dlamda = lamda2 - lamda1

    a = sin(dphi/2)**2 + cos(phi1)*cos(phi2)*(sin(dlamda/2)**2)
    c = 2 * arctan(sqrt(a) / sqrt(1 - a))
    d = R * c
    return d


def distance(p1, p2):
    """
    Calculate the distance in miles on a sphere from longitudes and latitudes.

    Based on the haversine formula:
    https://en.wikipedia.org/wiki/Haversine_formula

    Arguments:
        p1, p2: (latitude, longitude) tuples of the two points

    Latitude and longitude coordinates are represented as decimal numbers.
    The latitude is preceded by a minus sign (–) if it is south of the equator
    (a positive number implies north), and the longitude is preceded by a
    minus sign if it is west of the prime meridian (a positive number implies
    east).

    E.g. from p1 = (36.144698, -86.803177) and p2 = (36.144871, -86.793150)
    the calculated distance should be approximately 0.56 miles.
    """

    return haverside(p1, p2)


def main(filename):
    """
    Calculate key metrics of a route from a GPS teacking log.

    Print the overall distance (in miles), the average and the maximum
    speeds (in mph)
    """
    init_len = 1000
    raw_time, raw_latitude, raw_longitude = ([0]*init_len,
                                             [0]*init_len,
                                             [0]*init_len)

    with open(filename, newline='') as csvfile:
        parser = csv.reader(csvfile, delimiter=',')
        for idx, row in enumerate(parser):
            if idx == 0:
                # Header row
                pass
            else:
                raw_time[idx], raw_latitude[idx], raw_longitude[idx] = (
                    float(row[0]),
                    float(row[1]),
                    float(row[2]))

    time = [0] + [ele/3600 for ele in raw_time if ele != 0]
    latitude = [ele for ele in raw_latitude if ele != 0]
    longitude = [ele for ele in raw_longitude if ele != 0]
    assert(len(time) == len(latitude) and len(latitude) == len(longitude))

    overall_d = 0
    all_speeds = [0] * (len(latitude)-1)
    for i in range(len(latitude)-1):
        p1 = (latitude[i], longitude[i])
        p2 = (latitude[i+1], longitude[i+1])
        dt = time[i+1] - time[i]

        d = distance(p1, p2)

        overall_d += d

        all_speeds[i] = d / dt

    t_total = time[-1] - time[0]
    avg_speed = overall_d / t_total
    max_speed = max(all_speeds)

    # Should these be truncated or rounded?
    print("Distance: {:.1f} miles".format(overall_d))
    print("Average speed: {:.0f} mph".format(avg_speed))
    print("Maximum speed: {:.0f} mph".format(max_speed))


if __name__ == '__main__':
    main("gps_log.csv")
