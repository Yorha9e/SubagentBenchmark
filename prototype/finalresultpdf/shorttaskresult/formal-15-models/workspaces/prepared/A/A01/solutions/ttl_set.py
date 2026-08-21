"""Implement the public contract from TASKS.md."""
import collections
import math


def _check_number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a finite int or float")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        if type(capacity) is not int:
            raise TypeError("capacity must be a positive int")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity
        ttl = _check_number(ttl, "ttl")
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")
        self._ttl = ttl
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._clock = clock
        self._data = collections.OrderedDict()

    def _now(self):
        return _check_number(self._clock(), "clock result")

    def _purge(self):
        if not self._data:
            return self._now()
        now = self._now()
        expired = [value for value, deadline in self._data.items()
                   if deadline <= now]
        for value in expired:
            del self._data[value]
        return now

    def add(self, value):
        now = self._purge()
        if value in self._data:
            del self._data[value]
            self._data[value] = now + self._ttl
            return
        if len(self._data) >= self._capacity:
            self._data.popitem(last=False)
        self._data[value] = now + self._ttl

    def discard(self, value):
        self._purge()
        if value in self._data:
            del self._data[value]

    def __contains__(self, value):
        self._purge()
        return value in self._data

    def __len__(self):
        self._purge()
        return len(self._data)
