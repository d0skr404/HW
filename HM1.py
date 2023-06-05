import functools
import requests
import psutil

import memory_profiler
from collections import OrderedDict, defaultdict


def measure_memory_usage(f):
    '''Function to measure memory used when executing a function'''
    @functools.wraps(f)
    def wrapper(*args, **kwargs):
        memory_before = psutil.virtual_memory().used
        result = f(*args, **kwargs)
        memory_after = psutil.virtual_memory().used
        memory_diff = memory_after - memory_before
        print(f"Memory usage before function execution: {memory_before} byte")
        print(f"Memory usage after function execution: {memory_after} byte")
        print(f"Difference in memory usage: {memory_diff} byte")

        return result

    return wrapper


def lfu_cache(max_limit=64):
    cache = OrderedDict()
    frequency = defaultdict(int)
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            if cache_key in cache:
                return cache[cache_key]
            result = f(*args, **kwargs)
            cache[cache_key] = result
            frequency[cache_key] += 1
            if len(cache) > max_limit:
                min_freq_key = min(frequency, key=frequency.get)
                cache.pop(min_freq_key)
                frequency.pop(min_freq_key)
            return result
        return deco
    return internal


@lfu_cache(max_limit=64)
@measure_memory_usage
def fetch_url(url, first_n=100):
    """Fetch a given url"""
    res = requests.get(url)
    return res.content[:first_n] if first_n else res.content


fetch_url('https://www.youtube.com/',first_n = 100)