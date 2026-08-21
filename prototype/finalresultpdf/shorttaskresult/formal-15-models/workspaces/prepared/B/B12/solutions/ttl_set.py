"""Bounded TTL set with capacity eviction and time-based expiration."""

import math
from collections import OrderedDict


def _validate_number(val, allow_zero=True, label="value"):
    """Check that *val* is a finite int/float but not bool."""
    if isinstance(val, bool):
        raise TypeError(f"{label} must be a number, not bool")
    if not isinstance(val, (int, float)):
        raise TypeError(f"{label} must be int or float")
    if isinstance(val, float) and not math.isfinite(val):
        raise ValueError(f"{label} must be finite")
    if not allow_zero and val <= 0:
        raise ValueError(f"{label} must be positive")


class BoundedTTLSet:
    """A set-like container with bounded capacity and per-entry TTL.

    Parameters
    ----------
    capacity : int (not bool), > 0
    ttl : int or float (not bool), finite, >= 0
    clock : callable returning a finite int/float (not bool)
    """

    def __init__(self, capacity, ttl, clock):
        _validate_number(capacity, allow_zero=False, label="capacity")
        if isinstance(capacity, bool):
            raise TypeError("capacity must be int, not bool")
        _validate_number(ttl, allow_zero=True, label="ttl")
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")
        if not callable(clock):
            raise TypeError("clock must be callable")

        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._data = OrderedDict()  # key_object -> deadline

    def _get_now(self):
        """Read and validate current clock time."""
        now = self._clock()
        _validate_number(now, label="clock result")
        return now

    def _purge(self, now):
        """Remove all entries whose deadline <= *now*."""
        to_remove = [k for k, deadline in self._data.items() if now >= deadline]
        for k in to_remove:
            del self._data[k]

    def add(self, value):
        now = self._get_now()
        self._purge(now)

        # If an equal key exists, remove the old entry entirely
        # (this loses its position in insertion order)
        if value in self._data:
            del self._data[value]

        self._data[value] = now + self._ttl

        # Evict oldest if over capacity
        while len(self._data) > self._capacity:
            self._data.popitem(last=False)

    def discard(self, value):
        now = self._get_now()
        self._purge(now)
        self._data.pop(value, None)

    def __contains__(self, value):
        now = self._get_now()
        self._purge(now)
        return value in self._data

    def __len__(self):
        now = self._get_now()
        self._purge(now)
        return len(self._data)
