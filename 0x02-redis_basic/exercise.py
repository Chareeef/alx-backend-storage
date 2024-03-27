#!/usr/bin/python3
""" Implement the Cache class """
import redis
from typing import Union
from uuid import uuid4


class Cache:
    """ Encapsulate some Redis features """

    def __init__(self):
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
