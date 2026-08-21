"""Implement the public contract from TASKS.md."""

import math
from collections import OrderedDict


def _validate_numeric(value, name, allow_zero, positive_only):
    """Validate ttl/clock-result style numeric."""
    if type(value) is bool:
        raise TypeError(f"{name} must not be bool")
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be int or float")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    if positive_only and value <= 0:
        raise ValueError(f"{name} must be positive")
    if not allow_zero and value < 0:
        raise ValueError(f"{name} must be nonnegative")


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        if type(capacity) is bool or not isinstance(capacity, int):
            raise TypeError("capacity must be int")
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        _validate_numeric(ttl, "ttl", allow_zero=True, positive_only=False)
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")

        if not callable(clock):
            raise TypeError("clock must be callable")

        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._data = OrderedDict()  # key -> deadline

    def _now(self):
        t = self._clock()
        _validate_numeric(t, "clock()", allow_zero=True, positive_only=False)
        return t

    def _purge(self, now):
        to_del = [k for k, deadline in self._data.items() if now >= deadline]
        for k in to_del:
            del self._data[k]

    def add(self, value):
        now = self._now()
        self._purge(now)

        # If equal key already exists, remove old entry first to avoid stale refs
        if value in self._data:
            # Find and remove the existing key by equality
            for k in list(self._data.keys()):
                if k == value:
                    del self._data[k]
                    break

        deadline = now + self._ttl
        self._data[value] = deadline

        if len(self._data) > self._capacity:
            self._data.popitem(last=False)

    def discard(self, value):
        now = self._now()
        self._purge(now)
        self._data.pop(value, None)

    def __contains__(self, value):
        now = self._now()
        self._purge(now)
        return value in self._data

    def __len__(self):
        now = self._now()
        self._purge(now)
        return len(self._data)
