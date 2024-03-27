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
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function """

        # Increment by one the number of calls
        self.incr(key)

        # Call the store method and return its returned key
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """ Decorator to store the history of
    inputs and outputs for a particular function (Cache.store)
    """

    # Define inputs and outputs lists keys
    inputs_key = method.__qualname__ + ':inputs'
    outputs_key = method.__qualname__ + ':outputs'

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """ Wrapper function """

        # Store the inputs
        self.rpush(inputs_key, str(args))

        # Call the method and store the output
        outs = method(self, *args, **kwargs)
        self.rpush(outputs_key, outs)

        # Return the original output
        return outs

    # Return the wrapper
    return wrapper


class Cache:
    """ Encapsulate some Redis features """

    def __init__(self) -> None:
        """ Instantiate a Redis client and flush it """
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
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
        """ Increment the stored value in that key by 1 """
        self._redis.incr(key)

    def rpush(self, key: str, value: Union[str, bytes, int, float]) -> None:
        """ Right push the value to the list stored in that key """
        self._redis.rpush(key, value)
