"""Implement the public contract from TASKS.md."""

import collections
import math


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be a positive int")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        self._validate_finite_number(ttl, "ttl", nonnegative=True)
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._data = collections.OrderedDict()

    @staticmethod
    def _validate_finite_number(value, label="value", nonnegative=False):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{label} must be a number")
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError(f"{label} must be finite")
        if nonnegative and value < 0:
            raise ValueError(f"{label} must be nonnegative")
        return value

    def _now(self):
        t = self._clock()
        self._validate_finite_number(t, "clock()")
        return t

    def _purge(self, now):
        expired = [k for k, deadline in self._data.items() if now >= deadline]
        for k in expired:
            del self._data[k]

    def add(self, value):
        now = self._now()
        self._purge(now)
        if value in self._data:
            del self._data[value]
        self._data[value] = now + self._ttl
        while len(self._data) > self._capacity:
            self._data.popitem(last=False)

    def discard(self, value):
        now = self._now()
        self._purge(now)
        if value in self._data:
            del self._data[value]

    def __contains__(self, value):
        now = self._now()
        self._purge(now)
        return value in self._data

    def __len__(self):
        now = self._now()
        self._purge(now)
        return len(self._data)
