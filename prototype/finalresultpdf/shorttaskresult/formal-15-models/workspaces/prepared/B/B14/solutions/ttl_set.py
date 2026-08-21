"""Implement the public contract from TASKS.md."""

import math
from collections import OrderedDict


def _validate_number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(name + " must be a finite int or float, not bool")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(name + " must be finite")
    return value


class BoundedTTLSet:
    """A capacity-bounded set whose entries expire at a per-entry deadline."""

    def __init__(self, capacity, ttl, clock):
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be a positive int, not bool")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._capacity = capacity

        _validate_number(ttl, "ttl")
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")
        self._ttl = ttl

        if not callable(clock):
            raise TypeError("clock must be callable")
        self._clock = clock

        self._data = OrderedDict()

    def _read_now(self):
        now = self._clock()
        _validate_number(now, "clock()")
        return now

    def _purge(self, now):
        expired = [key for key, deadline in self._data.items() if now >= deadline]
        for key in expired:
            del self._data[key]

    def add(self, value):
        now = self._read_now()
        self._purge(now)
        if value in self._data:
            del self._data[value]
        self._data[value] = now + self._ttl
        while len(self._data) > self._capacity:
            self._data.popitem(last=False)

    def discard(self, value):
        now = self._read_now()
        self._purge(now)
        if value in self._data:
            del self._data[value]

    def __contains__(self, value):
        now = self._read_now()
        self._purge(now)
        return value in self._data

    def __len__(self):
        now = self._read_now()
        self._purge(now)
        return len(self._data)
