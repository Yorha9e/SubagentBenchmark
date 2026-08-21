"""Implement the public contract from TASKS.md."""

import math
from collections import OrderedDict


def _validate_number(value, label):
    if isinstance(value, bool):
        raise TypeError(f"{label} must not be a bool")
    if not isinstance(value, (int, float)):
        raise TypeError(f"{label} must be an int or float")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{label} must be finite")
    return value


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be an int")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        _validate_number(ttl, "ttl")
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        # Single source of truth: live key object -> deadline, in live
        # insertion order. No heaps, tombstones, or history queues that could
        # retain stale object references.
        self._entries = OrderedDict()

    def _current_time(self):
        return _validate_number(self._clock(), "clock result")

    def _purge(self, now):
        # The clock need not be monotonic, so scan every live entry instead of
        # stopping at the first unexpired one.
        expired = [key for key, deadline in self._entries.items() if now >= deadline]
        for key in expired:
            del self._entries[key]

    def add(self, value):
        now = self._current_time()
        self._purge(now)
        # Delete any equal key first so the new object replaces the stored
        # object, deadline, and insertion position (a plain assignment would
        # keep the old key object).
        if value in self._entries:
            del self._entries[value]
        self._entries[value] = now + self._ttl
        if len(self._entries) > self._capacity:
            self._entries.popitem(last=False)

    def discard(self, value):
        now = self._current_time()
        self._purge(now)
        self._entries.pop(value, None)

    def __contains__(self, value):
        now = self._current_time()
        self._purge(now)
        return value in self._entries

    def __len__(self):
        now = self._current_time()
        self._purge(now)
        return len(self._entries)
