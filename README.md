# `cachetory`

[![Tests](https://github.com/kpn/cachetory/actions/workflows/tests.yml/badge.svg)](https://github.com/kpn/cachetory/actions/workflows/tests.yml)
[![Code style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/kpn/cachetory)

## Quickstart

```python
from cachetory import serializers
from cachetory.backends import async_ as async_backends
from cachetory.caches.async_ import Cache


cache = Cache[int](
    serializer=serializers.from_url("pickle+zstd://?pickle-protocol=4&compression-level=3"),
    backend=(await async_backends.from_url("redis://localhost:6379")),
)
async with cache:
    await cache.set("foo", 42)
    assert await cache.get("foo") == 42
```

### Non-async

```python
from cachetory import serializers
from cachetory.backends import sync as sync_backends
from cachetory.caches.sync import Cache


cache = Cache[int](
    serializer=serializers.from_url("pickle+zstd://"),
    backend=sync_backends.from_url("redis://localhost:6379"),
)
with cache:
    cache.set("foo", 42)
    assert cache.get("foo") == 42
```

## Tutorial

### Supported operations

| Operation                                         |                                                          |
|:--------------------------------------------------|:---------------------------------------------------------|
| `get(key, default)`                               | Retrieve a value (or return a default one)               |
| `__getitem__(key)`                                | Retrieve a value or raise `KeyError` (only sync `Cache`) |
| `get_many(*keys)`                                 | Retrieve many values as a dictionary                     |
| `set(key, value, *, time_to_live, if_not_exists)` | Set a value and return if the value has been changed     |
| `__setitem__(key, value)`                         | Set a value (only sync `Cache`)                          |
| `set_many(items)`                                 | Set many values                                          |
| `expire_in(key, time_to_live)`                    | Set an expiration duration on a key                      |
| `delete(key)`                                     | Delete a key and return whether the key existed          |
| `__delitem__(key)`                                | Delete a key (only sync `Cache`)                         |

### Instantiating a `Cache`

Both sync and async `Cache`s requires at least these parameters to work:
- `backend`: functions as a storage
- `serializer`: is responsible for converting actual values from and to something that a backend would be able to store

`Cache` may be annotated with a value type, like this: `Cache[ValueT]`, which provides type hints for the cache methods.

### Instantiating a backend

There is a few ways to instantiate a backend:
- By directly instantiating a backend class via its `__init__`
- By instantiating a specific backend class via its `from_url` class method. In that case the URL is forwarded to underlying client (if any)
- By using `cachetory.[sync|async_].from_url` function. In that case specific backend class is chosen by the URL's scheme (see the scheme badges below), and the URL is forwarded to its `from_url` class method. This is especially useful to configure an arbitrary backend from a single configuration option – instead of hard-coding a specific backend class.

### Instantiating a serializer

Instantiating of a serializer is very much similar to that of a backend. To instantiate it by a URL use `cachetory.serializers.from_url` – unlike the back-end case there are no separate sync and async versions.

`cachetory.serializers.from_url` supports scheme joining with `+`, as in `pickle+zlib://`. In that case multiple serializers are instantiated and applied sequentially (in the example a value would be serialized by `pickle` and the serialized value is then compressed by `zlib`). Deserialization order is, of course, the opposite.

### Decorators

## Supported backends

### Redis: `cachetory.backends.sync.RedisBackend` and `cachetory.backends.async_.RedisBackend`

![scheme: redis](https://img.shields.io/badge/scheme-redis://-important)
![scheme: rediss](https://img.shields.io/badge/scheme-rediss://-important)
![scheme: redis+unix](https://img.shields.io/badge/scheme-redis+unix://-important)
![extra: redis-sync](https://img.shields.io/badge/sync-redis--sync-blue)
![extra: redis-async](https://img.shields.io/badge/async-redis--async-blueviolet)

The URL is forwarded to the underlying client, which means one can use whatever options the client provides. The only special case is `redis+unix://`: the leading `redis+` is first stripped and the rest is forwarded.

All the cache operations are atomic, including `get_many` and `set_many`.

### Memory: `cachetory.backends.sync.MemoryBackend` and `cachetory.backends.async_.MemoryBackend`

![scheme: memory](https://img.shields.io/badge/scheme-memory://-important)

### Dummy: `cachetory.backends.sync.DummyBackend` and `cachetory.backends.async_.DummyBackend`

![scheme: dummy](https://img.shields.io/badge/scheme-dummy://-important)

## Supported serializers

### Pickle: `cachetory.serializers.PickleSerializer`

![scheme: pickle](https://img.shields.io/badge/scheme-pickle://-important)

### No-operation: `cachetory.serializers.NoopSerializer`

![scheme: noop](https://img.shields.io/badge/scheme-noop://-important)
![scheme: null](https://img.shields.io/badge/scheme-null://-important)

`cachetory.serializers.NoopSerializer` does nothing and just bypasses value back and forth. Most of the backends don't support that and require some kind of serialization.

However, it is possible to use `NoopSerializer` with `MemoryBackend`, because the latter just stores all values in a Python dictionary and doesn't necessarily require values to be serialized.

## Supported compressors

**Compressor** is basically just a partial case of serializer: it's a serializer from `bytes` to and from `bytes`, which by definition provides some kind of data compression.

Compressors are packaged separately in `cachetory.serializers.compressors`.

## Zlib: `cachetory.serializers.compressors.ZlibCompressor`

![scheme: zlib](https://img.shields.io/badge/scheme-zlib://-important)

## Zstandard: `cachetory.serializers.compressors.ZstdCompressor`

![scheme: zstd](https://img.shields.io/badge/scheme-zstd://-important)
![scheme: zstandard](https://img.shields.io/badge/scheme-zstandard://-important)
![extra: zstd](https://img.shields.io/badge/extra-zstd-blue)
