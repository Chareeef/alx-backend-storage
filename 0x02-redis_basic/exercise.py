#!/usr/bin/env python3
""" Implement the Cache class """
import redis
from typing import Any, Callable, Union
from uuid import uuid4


class Cache:
    """ Encapsulate some Redis features """

    def __init__(self) -> None:
        """ Instantiate a Redis client and flush it """
        self._redis = redis.Redis()
        self._redis.flushdb()

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
