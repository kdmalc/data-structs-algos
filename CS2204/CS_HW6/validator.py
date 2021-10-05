#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Validator script for CS 2204 Homework submissions"""
from math import isclose
from functools import lru_cache
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
                if partial == 0:
                    abort = getattr(test, "__abort__", False)
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
@lru_cache()
def _load_dataset(filename):
    """Caching load results to speed-up testing"""
    module = import_file("movies.py")
    return module.load_dataset("movies.json")


@points(10)
def test_unrated_movies():
    """Testing unrated_movies"""
    module = import_file("movies.py")
    movies, users = _load_dataset("movies.json")

    expected = [
        'Corpo celeste', 'Sugar Hill', 'The Journey', 'The Cat', 'Amigo',
        "Coluche, l'histoire d'un mec", 'Bana Masal Anlatma',
        'Road to Victory', 'Play Dirty', 'Dil', 'Addicted to Sexting',
        "Ghosts Can't Do It", 'Lucky Jordan', 'Kovat Miehet',
        'Full Body Massage',
        'Murder in New Hampshire: The Pamela Wojas Smart Story',
        'The Young Lady and the Hooligan', 'The Invicible Cell',
        'The Story of Asya Klyachina', 'Autumn Tale', 'The Visit', 'Thirst',
        'The Bank', 'Monsieur Batignole', 'Murder of a Cat',
        "The Kaiser's Lackey", 'The Egg and I', 'Little Moscow', 'Heart',
        "Bottled Life: Nestle's Business with Water", 'Rags',
        'Echoes From a Sombre Empire', 'Same Same But Different',
        'Hate for Hate', 'San Giovanni decollato', 'Darling Lili',
        'The Strange Saga of Hiroshi the Freeloading Sex Machine',
        'Leviathan: The Story of Hellraiser and Hellbound: Hellraiser II',
        'Hotte in Paradise', 'Meet the Fokkens', 'The Secret Game', 'Who?'
    ]

    returned = module.unrated_movies(movies, users)
    assert set(expected) == set(returned)


@points(15)
def test_most_rated_movies():
    """Testing most_rated_movies"""
    module = import_file("movies.py")
    movies, users = _load_dataset("movies.json")

    expected_8 = [
        'Forrest Gump', 'The Shawshank Redemption', 'Pulp Fiction',
        'The Silence of the Lambs', 'The Matrix', 'Star Wars',
        'Jurassic Park', "Schindler's List"
    ]

    returned_8 = module.most_rated_movies(movies, users, n_top=8)
    assert set(expected_8) == set(returned_8)

@points(20)
def test_highest_rated_movies():
    """Testing highest_rated_movies"""
    module = import_file("movies.py")
    movies, users = _load_dataset("movies.json")

    expected_7_200 = [
        'The Shawshank Redemption', 'The Godfather', 'The Usual Suspects',
        'Seven Samurai', 'The Third Man', 'The Godfather: Part II',
        "Schindler's List"
    ]

    returned_7_200 = module.highest_rated_movies(movies, users,
                                                 n_top=7, n_min_ratings=200)
    assert set(expected_7_200) == set(returned_7_200)

    expected_6_10 = [
        'Hands on a Hard Body: The Documentary', 'Whiplash', 'Planet Earth',
        'Ivan Vasilyevich Changes His Profession', "I Know Where I'm Going!",
        'Maya Lin: A Strong Clear Vision'
    ]
    returned_6_10 = module.highest_rated_movies(movies, users,
                                                n_top=6, n_min_ratings=10)

    assert set(expected_6_10) == set(returned_6_10)


@points(20)
def test_most_popular_genres():
    """Testing most_popular_genres"""
    module = import_file("movies.py")
    movies, users = _load_dataset("movies.json")

    expected_3 = ['History', 'War', 'Documentary']
    returned_3 = module.most_popular_genres(movies, users, n_top=3)
    assert set(expected_3) == set(returned_3)

    expected_7 = ['History', 'War', 'Documentary', 'Drama',
                  'Crime', 'Mystery', 'Animation']
    returned_7 = module.most_popular_genres(movies, users, n_top=7)
    assert set(expected_7) == set(returned_7)


@points(15)
def test_taste_similarity():
    """Testing taste_similarity"""
    module = import_file("movies.py")
    movies, users = _load_dataset("movies.json")

    user1 = users["u85100"]
    user2 = users["u118051"]
    assert isclose(module.taste_similarity(user1, user2), 0.17288597670662736)

    user1 = users["u30444"]
    user2 = users["u233004"]
    assert isclose(module.taste_similarity(user1, user2), 0.4280398171973992)

    user1 = users["u135796"]
    user2 = users["u143528"]
    assert isclose(module.taste_similarity(user1, user2), 0.016948855331273414)

    user1 = users["u227923"]
    user2 = users["u108386"]
    assert isclose(module.taste_similarity(user1, user2), 0.0)


@points(20)
def test_suggest_movie():
    """Testing suggest_movie"""
    module = import_file("movies.py")
    movies, users = _load_dataset("movies.json")

    new_user = {
        'tt0109127': 1.5,
        'tt0078841': 3.0,
        'tt0076054': 0.5,
        'tt0061852': 4.5,
        'tt0063823': 4.0,
        'tt0105417': 3.0,
        'tt0094142': 4.5,
        'tt0108037': 4.0,
        'tt0074174': 5.0,
        'tt0317303': 3.5,
        'tt0062803': 4.5,
        'tt0056262': 3.0,
        'tt0396752': 1.0,
        'tt1499658': 4.0,
        'tt0848228': 5.0,
        'tt1392170': 4.5,
        'tt0948470': 5.0,
        'tt0454876': 0.5
    }

    returned = module.suggest_movie(movies, users, new_user)
    assert returned == "Silver Linings Playbook"

    new_user = {
        'tt0083658': 4.0,
        'tt0068646': 5.0,
        'tt0120373': 2.0,
        'tt0118688': 1.0,
        'tt0119695': 2.0,
        'tt0089173': 1.0,
        'tt0120577': 2.0,
        'tt0181865': 3.0}

    returned = module.suggest_movie(movies, users, new_user)
    assert returned == "Crouching Tiger, Hidden Dragon"


@points(-10)
def test_author():
    """Checking author information"""
    module = import_file("movies.py")
    author = getattr(module, "__author__", None)
    assert isinstance(author, str) and author, \
        "__author__ variable is not set properly"


def test_pep8():
    """Checking PEP8 style"""

    n_errors, msgs = check_pep8_style("movies.py")
    if n_errors:
        print(msgs)
        return -n_errors


if __name__ == "__main__":
    validate(
        test_unrated_movies,
        test_most_rated_movies,
        test_highest_rated_movies,
        test_most_popular_genres,
        test_taste_similarity,
        test_suggest_movie,
        test_author,
        test_pep8,
    )
