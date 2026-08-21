"""Implement the public contract from TASKS.md."""

import math
from collections import OrderedDict


def _validate_capacity(capacity):
    if isinstance(capacity, bool) or not isinstance(capacity, int):
        raise TypeError("capacity must be a positive int")
    if capacity <= 0:
        raise ValueError("capacity must be positive")


def _validate_ttl(ttl):
    if isinstance(ttl, bool) or not isinstance(ttl, (int, float)):
        raise TypeError("ttl must be a finite number")
    if not math.isfinite(ttl):
        raise ValueError("ttl must be finite")
    if ttl < 0:
        raise ValueError("ttl must be nonnegative")


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        _validate_capacity(capacity)
        _validate_ttl(ttl)
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._entries = OrderedDict()

    def _purge(self):
        now = self._clock()
        expired = [key for key, deadline in self._entries.items() if now >= deadline]
        for key in expired:
            del self._entries[key]

    def add(self, value):
        self._purge()
        if value in self._entries:
            del self._entries[value]
        elif len(self._entries) >= self._capacity:
            self._entries.popitem(last=False)
        self._entries[value] = self._clock() + self._ttl

    def discard(self, value):
        self._purge()
        self._entries.pop(value, None)

    def __contains__(self, value):
        self._purge()
        return value in self._entries

    def __len__(self):
        self._purge()
        return len(self._entries)
