#!/usr/bin/env python3
""" Implement get_page function """
import redis
import requests


def get_page(url: str) -> str:
    """ Obtain the HTML content of a particular URL and return it
    Also track how many times a particular URL was accessed
    """

    # Instantiate redis
    r = redis.Redis()

    # Define the count key
    key = f'count:{url}'

    # Get old count
    count = r.get(key)

    # Set count with an expiration time of 10 seconds
    if not count:
        r.setex(key, 10, 1)
    else:
        r.setex(key, 10, int(count) + 1)

    # Return the page
    return requests.get(url)
