# Redis - Basic

Welcome to the world of Redis! In this README, we'll dive into the basics of Redis, covering how to use it for basic operations with `redis-cli`, leveraging it as a simple cache, and communicating with Redis using `redis-py`. Let's get started!

## Using Redis for Basic Operations (with redis-cli)

Redis provides a powerful command-line interface (`redis-cli`) that allows us to interact with Redis servers easily. It's like having a direct line to our Redis database where we can execute commands and perform various operations.

### Installation

First things first, we need to ensure we have Redis installed on our system. We can install it using our system's package manager or by downloading it from the official Redis website.

Once installed, we can launch the Redis CLI by simply typing `redis-cli` in our terminal.

### Basic Commands

Redis supports various data types and commands. Here are some basic commands to get we started:

#### Set and Get

```bash
# Set a key-value pair
> SET mykey "Hello, Redis!"

# Retrieve the value for a key
> GET mykey
```

#### Lists

```bash
# Push elements to a list
> LPUSH mylist "item1"
> LPUSH mylist "item2"

# Retrieve elements from a list
> LRANGE mylist 0 -1
```

#### Sets

```bash
# Add elements to a set
> SADD myset "member1"
> SADD myset "member2"

# Retrieve members of a set
> SMEMBERS myset
```

#### Sorted Sets

Sorted sets are similar to sets but are ordered by their score, allowing for range queries and retrieval of elements in a specific order.

```bash
# Add elements with scores to a sorted set
> ZADD mysortedset 1 "one"
> ZADD mysortedset 2 "two"
> ZADD mysortedset 3 "three"

# Retrieve elements from the sorted set in ascending order
> ZRANGE mysortedset 0 -1
```

#### Hashes

Hashes are maps between string fields and string values, ideal for representing objects with multiple attributes.

```bash
# Set multiple field-value pairs in a hash
> HMSET myhash field1 "value1" field2 "value2"

# Retrieve all field-value pairs from the hash
> HGETALL myhash
```

### Redis as a Simple Cache

Redis is commonly used as a cache due to its fast read and write operations. Let's see how we can use Redis to implement a simple caching mechanism in our applications.

#### Cache Example with redis-cli

```bash
# Set a key-value pair with expiration (cache for 1 hour)
> SET my_cached_data "Hello, Redis! This is cached data" EX 3600

# Retrieve the cached data
> GET my_cached_data
```

### Talking to Redis through redis-py

`redis-py` is a Python library that allows us to interact with Redis from Python code. It provides a convenient interface for executing Redis commands and managing connections.

#### Installation

You can install `redis-py` using pip:

```bash
pip install redis
```

#### Usage

```python
import redis

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Set a key
r.set('mykey', 'Hello, Redis!')

# Get the value for a key
value = r.get('mykey')
print(value)
```

With `redis-py`, we can perform all sorts of operations on Redis, just like we would with `redis-cli`, but directly from our Python code.

## Conclusion

We've just scratched the surface of what Redis has to offer. We now know how to perform basic operations using `redis-cli`, leverage Redis as a simple cache, and communicate with Redis through `redis-py`. Keep exploring, and have fun building awesome applications with Redis! 😁
