"""Implement the public contract from TASKS.md."""

import math
from collections import OrderedDict


def _validate_finite_number(value, name):
    if type(value) is bool or type(value) not in (int, float):
        raise TypeError(f"{name} must be a finite int or float, not bool")
    if type(value) is float and not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        if type(capacity) is not int or isinstance(capacity, bool):
            raise TypeError("capacity must be an int but not bool")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        _validate_finite_number(ttl, "ttl")
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")
        if not callable(clock):
            raise TypeError("clock must be callable")

        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._entries = OrderedDict()

    def _now(self):
        current = self._clock()
        _validate_finite_number(current, "clock")
        return current

    def _purge(self, now):
        expired = [key for key, deadline in self._entries.items() if now >= deadline]
        for key in expired:
            del self._entries[key]

    def _remove_equal(self, value):
        for key in list(self._entries):
            if key == value:
                del self._entries[key]
                return

    def add(self, value):
        now = self._now()
        self._purge(now)
        self._remove_equal(value)
        self._entries[value] = now + self._ttl
        while len(self._entries) > self._capacity:
            self._entries.popitem(last=False)

    def discard(self, value):
        now = self._now()
        self._purge(now)
        self._remove_equal(value)

    def __contains__(self, value):
        now = self._now()
        self._purge(now)
        for key in self._entries:
            if key == value:
                return True
        return False

    def __len__(self):
        now = self._now()
        self._purge(now)
        return len(self._entries)
