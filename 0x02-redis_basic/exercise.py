#!/usr/bin/env python3
""" Implement the Cache class """
from functools import wraps
import redis
from typing import Any, Callable, Union
from uuid import uuid4


def count_calls(method: Callable) -> Callable:
    """ Decorator for store method that increments the count
    for the __qualname__ key every time the method is called

    Return the value returned by the original method
    """
    
    @wraps(method)
    def wrapper(self, data: Union[str, bytes, int, float]) -> str:
        """ Wrapper function """
        key = method.__qualname__

        # Initialize counter to 0 if not done
        if not self.get_int(key):
            self.set(key, 0)

        # Increment by one the number of calls
        self.incr(key)

        # Call the store method and return its returned key
        return method(self, data)

    return wrapper


class Cache:
    """ Encapsulate some Redis features """

    def __init__(self) -> None:
        """ Instantiate a Redis client and flush it """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Generate a random key, store the input data in
        Redis using the random key and return the key
        """

        # Generate the key using uuid4
        key = str(uuid4())

        # Store it in the Redis database
        self._redis.set(key, data)

        # Return the key
        return key

    def get(self, key: str, fn: Callable = None) -> Any:
        """ Take a key string argument and return the stored value if any """

        # Retrieve value
        value = self._redis.get(key)

        # Format with `fn` if relevant
        if value and fn:
            value = fn(value)

        # Return the value
        return value

    def get_str(self, key: str) -> Union[str, None]:
        """ Get and return the string value stored in key """
        return self.get(key, str)

    def get_int(self, key: str) -> Union[int, None]:
        """ Get and return the integer value stored in key """
        return self.get(key, int)

    def set(self, key: str, value: Union[str, bytes, int, float]) -> None:
        """ Set a key-value pair """
        self._redis.set(key, value)

    def incr(self, key: str) -> None:
        """ Increment the stored value stored in that key by 1 """
        return self._redis.incr(key)
