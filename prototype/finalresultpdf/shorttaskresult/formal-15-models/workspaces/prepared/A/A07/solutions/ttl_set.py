"""Implement the public contract from TASKS.md."""

import math
from collections import OrderedDict


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be an int")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if isinstance(ttl, bool) or not isinstance(ttl, (int, float)):
            raise TypeError("ttl must be an int or float")
        if isinstance(ttl, float) and not math.isfinite(ttl):
            raise ValueError("ttl must be finite")
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")
        if not callable(clock):
            raise TypeError("clock must be callable")

        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._entries = OrderedDict()

    @staticmethod
    def _validate_time(value):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError("clock must return an int or float")
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError("clock must return a finite number")
        return value

    def _now(self):
        return self._validate_time(self._clock())

    def _purge(self, now):
        expired = [
            key for key, (_, deadline) in self._entries.items() if now >= deadline
        ]
        for key in expired:
            self._entries.pop(key, None)

    def add(self, value):
        now = self._now()
        deadline = now + self._ttl
        self._purge(now)

        if value in self._entries:
            self._entries.pop(value)
        elif len(self._entries) >= self._capacity:
            self._entries.popitem(last=False)

        self._entries[value] = (value, deadline)

    def discard(self, value):
        now = self._now()
        self._purge(now)
        self._entries.pop(value, None)

    def __contains__(self, value):
        now = self._now()
        self._purge(now)
        return value in self._entries

    def __len__(self):
        now = self._now()
        self._purge(now)
        return len(self._entries)
