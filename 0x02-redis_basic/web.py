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
        key_count = f'count:{url}'

        # Get old count
        count = int(r.get(key_count) or 0)

        # Track number of visits to `url`
        r.set(key_count, count + 1, ex=10)

        # Return fn's result
        return fn(url)

    return wrapper


@count_visits
def get_page(url: str) -> str:
    """ Obtain the HTML content of a particular URL and return it """

    # Instantiate redis
    r = redis.Redis()

    # Try to get cached web_page
    page = r.get(url)

    # If doesn't exist, get and cache with an expiration time of 10 seconds
    if not page:
        page = requests.get(url).text
    else:
        page = page.decode('utf-8')

    r.setex(url, 10, page)

    # Return the page
    return page


if __name__ == '__main__':
    from time import sleep
    r = redis.Redis()
    r.flushdb()

    url = 'http://slowwly.robertomurray.co.uk'

    for _ in range(20):
        print(get_page(url)[:20])
        print('\n   COUNT:', r.get(f'count:{url}'))
        sleep(1)
