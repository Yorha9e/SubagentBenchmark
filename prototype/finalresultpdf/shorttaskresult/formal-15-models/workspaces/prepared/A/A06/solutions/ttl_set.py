"""Implement the public contract from TASKS.md."""

import math


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        if type(capacity) is not int:
            raise TypeError("capacity must be an int")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if type(ttl) not in (int, float):
            raise TypeError("ttl must be an int or float")
        if not math.isfinite(ttl):
            raise ValueError("ttl must be finite")
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._entries = {}  # stored object -> deadline, in insertion order

    def _now(self):
        moment = self._clock()
        if type(moment) not in (int, float):
            raise TypeError("clock results must be int or float")
        if not math.isfinite(moment):
            raise ValueError("clock results must be finite")
        return moment

    def _purge(self, moment):
        expired = [key for key, deadline in self._entries.items() if moment >= deadline]
        for key in expired:
            del self._entries[key]

    def add(self, value):
        moment = self._now()
        self._purge(moment)
        deadline = moment + self._ttl
        if value in self._entries:
            del self._entries[value]
        elif len(self._entries) >= self._capacity:
            del self._entries[next(iter(self._entries))]
        self._entries[value] = deadline

    def discard(self, value):
        moment = self._now()
        self._purge(moment)
        self._entries.pop(value, None)

    def __contains__(self, value):
        moment = self._now()
        self._purge(moment)
        return value in self._entries

    def __len__(self):
        moment = self._now()
        self._purge(moment)
        return len(self._entries)
