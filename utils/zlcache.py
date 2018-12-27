# encoding: utf-8
# zlcache.py by Anderson Huang at 2018/12/27 15:22
import memcache

"""
创建memcached缓存机制
"""

cache = memcache.Client(['192.168.1.114:11221'], debug=True)


def set(key, value, timeout=0):
    return cache.set(key, value, timeout)


def get(key):
    return cache.get(key)


def delete(key):
    return cache.delete(key)
