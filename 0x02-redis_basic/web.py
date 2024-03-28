#!/usr/bin/env python3
""" Implement get_page function """
from functools import wraps
import redis
import requests
from typing import Callable


def count_visits(fn: Callable) -> Callable:
    """ Decorator to track how many times a particular URL was accessed """

    @wraps(fn)
    def wrapper(url):
        """ Wrapper function """

        # Instantiate redis
        r = redis.Redis()

        # Define the count key
        key_count = 'count:{' + url + '}'

        # Get old count
        count = int(r.get(key_count) or 0)

        # Track number of visits to `url`
        r.set(key_count, count + 1)

        # Return fn's result
        return fn(url)

    return wrapper


@count_visits
def get_page(url: str) -> str:
    """ Obtain the HTML content of a particular URL and return it """

    # Instantiate redis
    r = redis.Redis()

    # Try to get cached web_page
    bytes_resp = r.get(url)

    # If doesn't exist, get and cache with an expiration time of 10 seconds
    if not bytes_resp:

        try:
            resp = requests.get(url)

            if resp.status_code == 200:
                page = str(resp.text)
                r.setex(url, 10, page)
            else:
                return ''

        except Exception:
            return ''

    else:
        page = bytes_resp.decode('utf-8')

    # Return the page
    return page
