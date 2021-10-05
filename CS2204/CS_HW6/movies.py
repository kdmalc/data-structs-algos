#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Movies and Ratings - Building a Simple Recommender System"""

__author__ = "malcolkd"

import json
from collections import OrderedDict
import itertools
from math import sqrt


def convert_idents_to_titles(my_idents, movies):
    my_titles = set()
    for ident in my_idents:
        for movie_list in movies.items():
            if movie_list[0] == ident:
                my_titles.add(movie_list[1]['title'])
    return my_titles


def load_dataset(filename):
    """
    Load the dataset and return a (movies, users) tuple.

    Source: Kaggle - The Movies Dataset
            https://www.kaggle.com/rounakbanik/the-movies-dataset
            License: Creative Commons CC0 1.0
    """
    with open(filename, encoding="utf-8") as json_file:
        dataset = json.load(json_file)

    return dataset["movies"], dataset["users"]


def unrated_movies(movies, users):
    """Return a list of movie titles which have no ratings in the dataset"""
    my_rated_movie_set = set()
    for user_val_dict in users.values():
        for movie_ident in user_val_dict.keys():
            my_rated_movie_set.add(movie_ident)

    all_movies_set = set()
    for movie_ident in movies.keys():
        all_movies_set.add(movie_ident)

    # Use the set difference ("ven diagram") operation
    unrated_movie_identifiers = all_movies_set - my_rated_movie_set

    # Manual approach, not needed anymore
    """
    unrated_movies_titles = set()
    for ident in unrated_movie_identifiers:
        for movie_list in movies.items():
            if movie_list[0] == ident:
                unrated_movies_titles.add(movie_list[1]['title'])
    """

    umt_func = convert_idents_to_titles(unrated_movie_identifiers, movies)
    # assert umt_func == unrated_movies_titles

    return umt_func


def most_rated_movies(movies, users, n_top=10):
    """
    Return a list of n_top movie titles with the most rating data points

    Note: the actual rating values are not important, just the number of these.
    """
    my_rated_movie_list = []
    for user_val_dict in users.values():
        for movie_ident in user_val_dict.keys():
            my_rated_movie_list.append(movie_ident)

    num_ratings_per_movie = {}
    for movie_ident in my_rated_movie_list:
        num_ratings_per_movie[movie_ident] = num_ratings_per_movie.setdefault(
            movie_ident, -1) + 1

    sorted_ratings_dict = OrderedDict(sorted(
        num_ratings_per_movie.items(),
        key=lambda item: item[1],
        reverse=True))

    top_n_ratings_dict = OrderedDict(
        itertools.islice(
            sorted_ratings_dict.items(), n_top))

    most_ratings_list = []
    most_rated_titles = convert_idents_to_titles(
        top_n_ratings_dict.keys(), movies)

    for title in most_rated_titles:
        most_ratings_list.append(title)

    return most_ratings_list


def highest_rated_movies(movies, users, n_top=10, n_min_ratings=50):
    """
    Return a list of n_top highest rated movies based on their average ratings.

    The movie has to have at least n_min_ratings to consider in this ranking.
    """

    # Assemble all the movie ratings under the titles
    movie_ratings_dict = dict()
    for user_val_dict in users.values():
        for user in user_val_dict.items():
            try:
                movie_ratings_dict.setdefault(user[0], [])
                movie_ratings_dict[user[0]].append(user[1])
            except KeyError:
                print("Key Error!")
                movie_ratings_dict.setdefault(user[0], [])

    # Throw out the ones that don't meet n_min via list (dict?) comp
    more_than_min = [(key, val) for (key, val) in movie_ratings_dict.items()
                     if len(val) > n_min_ratings]

    # Get the average rating
    my_keys = [ele[0] for ele in more_than_min]
    my_vals = [sum(ele[1])/len(ele[1]) for ele in more_than_min]
    average_ratings_dict = dict(zip(my_keys, my_vals))

    # Sort
    sorted_ratings_dict = OrderedDict(sorted(
        average_ratings_dict.items(),
        key=lambda item: item[1],
        reverse=True))

    # Take the top n
    top_rated_dict = OrderedDict(
        itertools.islice(
            sorted_ratings_dict.items(), n_top))

    # Now switch from idents to strings
    highest_rated_titles = convert_idents_to_titles(
        top_rated_dict.keys(), movies)

    highest_ratings_list = []
    for title in highest_rated_titles:
        highest_ratings_list.append(title)

    return highest_ratings_list


def most_popular_genres(movies, users, n_top=10):
    """
    Return a list of the n_top genres based on the average ratings.

    The average rating of a genre is the average of the ratings of all those
    movies which belong to this genre. Note: a movie can belong to multiple
    genres.
    """

    # Get all the genres as a set
    genre_set = set()
    top_genres = OrderedDict()
    for movie_vals in movies.values():
        for genre in movie_vals['genres']:
            genre_set.add(genre)
            top_genres.setdefault(genre, 0)

    # Break up the movies into their respective genres
    genre_dict = {genre: dict() for genre in genre_set}
    for movie_tuple in movies.items():
        movie_ident = movie_tuple[0]
        movie_title = movie_tuple[1]['title']
        movie_genres = movie_tuple[1]['genres']
        for genre in movie_genres:
            genre_dict[genre].setdefault(movie_ident, movie_title)

    # Assemble all the movie ratings under the titles
    movie_ratings_dict = dict()
    for user_val_dict in users.values():
        for user in user_val_dict.items():
            movie_ratings_dict.setdefault(user[0], [])
            movie_ratings_dict[user[0]].append(user[1])

    for genre_tuple in genre_dict.items():
        my_genre = genre_tuple[0]
        genre_movies = genre_tuple[1]

        # Get a "sub dictionary"
        genre_ratings_dict = {key: value for key, value
                              in movie_ratings_dict.items()
                              if key in genre_movies.keys()}

        my_ratings = []
        [my_ratings.extend(val_list) for val_list
         in genre_ratings_dict.values()]

        top_genres[my_genre] = sum(my_ratings)/len(my_ratings)

    # Sort
    sorted_ratings_dict = OrderedDict(sorted(
        top_genres.items(),
        key=lambda item: item[1],
        reverse=True))

    # Take the top n
    top_rated_dict = OrderedDict(
        itertools.islice(
            sorted_ratings_dict.items(), n_top))
    return top_rated_dict.keys()


def taste_similarity(user1, user2):
    """
    Calculate the cosine similarity similarity between two users' ratings.

    If a movie is not rated by both users, use 0 for the missing rating.
    """
    user1_movies = list(user1.keys())
    user2_movies = list(user2.keys())
    all_movies_set = set(user1_movies + user2_movies)

    # Set operation: intersection
    shared_movies = set(user1_movies) & set(user2_movies)
    if len(shared_movies) == 0:
        return 0

    num = 0
    denom1 = 0
    denom2 = 0
    for movie in all_movies_set:
        num += (user1.get(movie, 0) * user2.get(movie, 0))
        denom1 += (user1.get(movie, 0)**2)
        denom2 += (user2.get(movie, 0)**2)
    cos_sim = num / (sqrt(denom1) * sqrt(denom2))

    if cos_sim > 1:
        cos_sim = 1
    elif cos_sim < 0:
        cos_sim = 0
    return cos_sim


def suggest_movie(movies, users, new_user):
    """
    Suggest a movie title based on the new_user's existing ratings.

    The suggestion is based on collaborative filtering. First, find a user
    in the ratings database which has the closest taste of the current user.
    Then, return the movie title with the highest rating from that user, which
    is not rated by the current user, yet. If all movies are rated by new_user,
    return None.
    """
    # Find another user in the database with a similar taste
    max_user = list(users.values())[0]
    for meta_user_dict in users.values():
        # Maybe do max instead of threshold? Instructions unclear
        if (taste_similarity(meta_user_dict, new_user) >
                taste_similarity(max_user, new_user)):
            max_user = meta_user_dict
    meta_user_dict = max_user
    # Find the movie rated highest by the meta_user
    meta_user_movies = set(meta_user_dict.keys())
    new_user_movies = set(new_user.keys())
    # Set operation: difference
    meta_only_movies = meta_user_movies - new_user_movies
    # Now get the above movies as a subdictionary, then sort
    meta_only_movies_dict = {key: value for key, value
                             in meta_user_dict.items()
                             if key in meta_only_movies}
    # Sort
    sorted_ratings_dict = OrderedDict(sorted(
        meta_only_movies_dict.items(),
        key=lambda item: item[1],
        reverse=True))
    # Take the top movie
    recommended_movie_dict = OrderedDict(
        itertools.islice(
            sorted_ratings_dict.items(), 1))

    title_set = convert_idents_to_titles(recommended_movie_dict.keys(), movies)
    for x in title_set:
        return x


if __name__ == "__main__":
    movies, users = load_dataset("movies.json")
