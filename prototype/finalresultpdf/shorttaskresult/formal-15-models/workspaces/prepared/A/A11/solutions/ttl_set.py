"""Implement the public contract from TASKS.md."""

import math


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be an int (not bool)")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if not callable(clock):
            raise TypeError("clock must be callable")
        if isinstance(ttl, bool) or not isinstance(ttl, (int, float)):
            raise TypeError("ttl must be int or float (not bool)")
        if math.isnan(ttl) or math.isinf(ttl) or ttl < 0:
            raise ValueError("ttl must be finite and nonnegative")
        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        # Insertion-ordered map: value -> deadline.
        self._data = {}

    def _now(self):
        t = self._clock()
        if isinstance(t, bool) or not isinstance(t, (int, float)):
            raise TypeError("clock result must be int or float (not bool)")
        if math.isnan(t) or math.isinf(t):
            raise ValueError("clock result must be finite")
        return t

    def _purge(self):
        now = self._now()
        expired = [k for k, deadline in self._data.items() if now >= deadline]
        for k in expired:
            del self._data[k]

    def add(self, value):
        self._purge()
        if value in self._data:
            del self._data[value]
            self._data[value] = self._now() + self._ttl
        else:
            if len(self._data) >= self._capacity:
                oldest = next(iter(self._data))
                del self._data[oldest]
            self._data[value] = self._now() + self._ttl

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
