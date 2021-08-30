# -*- coding: utf-8 -*-
"""
Created on Mon Aug 30 10:05:23 2021

@author: malcolkd
8/30/21: Classwork 1

Problem Description:
Princess must marry a prince, and there are many suitors
If she rejects, the suitor gets beheaded, so she can't go back

PROVEN SOLUTION: MAXIMALIST:
if choice == max(choice):
    score += 1 /N
Theoretical Optimum: ~37%
1/e * N

Could change this to "better than average" instead of "best" (max)
score += choice / N
Theoretical Optimum: sqrt(N)
"""

from random import gauss
import matplotlib.pyplot as plt


# Let's say she judges on height only, which follows a Gaussian Dist
"""
from random import gauss
gauss(6, 1) # (mean, variance)


suitors = [gauss(6, 1) for _ in range(100)]

import matplotlib.pyplot as plt


plt.stem(suitors)
plt.hist(suitors)

suitors1000 = [gauss(6, 1) for _ in range(100)]
plt.stem(suitors1000)
plt.hist(suitors1000)
"""


def summon_suitors(n_suitors=100):
    return [gauss(6, 1) for _ in range(n_suitors)]


def pick_a_prince(suitors, explore=10.0):
    # explore = 10.0 (%) implies we will explore 10 first to get an idea
    bar = -1
    for i, suitor in enumerate(suitors):
        # Need enumerate to tell whether you are in exploration or exploit

        # If below the threshold, we are still exploring
        if i < explore / 100.0 * len(suitors):
            bar = max(bar, suitor)
        elif suitor >= bar:
            return suitor
    # If we didn't find anyone, then just return the last guy
    return suitor


if __name__ == "__main__":
    suitors = summon_suitors()
    plt.stem(suitors)
    print("Best suitor:", max(suitors))
    print("Out pick:", pick_a_prince(suitors))

    scores = []
    for explore in range(100):
        score = 0
        for trial in range(1000):
            suitors = summon_suitors()
            prince = pick_a_prince(suitors, explore)

            # E.g. our picked prince was the tallest possible in the set
            if prince == max(suitors):
                score += 1
        scores.append(score)

    plt.figure()
    plt.xlabel("Threshold")
    plt.ylabel("Score")
    plt.plot(scores)
