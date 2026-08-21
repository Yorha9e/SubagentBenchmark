"""Implement the public contract from TASKS.md."""

import math
from collections import OrderedDict


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError("capacity must be an int")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if not isinstance(ttl, (int, float)) or isinstance(ttl, bool):
            raise TypeError("ttl must be an int or float")
        if not math.isfinite(ttl) or ttl < 0:
            raise ValueError("ttl must be finite and nonnegative")
        if not callable(clock):
            raise TypeError("clock must be callable")

        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._data = OrderedDict()

    def _validate_time(self, value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("clock result must be a finite int or float")
        if not math.isfinite(value):
            raise ValueError("clock result must be finite")

    def _purge(self):
        now = self._clock()
        self._validate_time(now)
        while self._data:
            value, deadline = next(iter(self._data.items()))
            if now >= deadline:
                self._data.popitem(last=False)
            else:
                break

    def add(self, value):
        self._purge()
        now = self._clock()
        self._validate_time(now)

        if value in self._data:
            del self._data[value]
        self._data[value] = now + self._ttl

        while len(self._data) > self._capacity:
            self._data.popitem(last=False)

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
