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

    # Try to get cached web_page
    page = r.get(url)

    # If doesn't exist, get and cache with an expiration time of 10 seconds
    if not page:
        page = requests.get(url)
        r.setex(url, 10, str(page))

    # Define the count key
    key_count = f'count:{url}'

    # Get old count
    count = r.get(key_count)

    # Track number of visits to `url`
    r.incr(key_count)

    # Return the page
    return str(page)
