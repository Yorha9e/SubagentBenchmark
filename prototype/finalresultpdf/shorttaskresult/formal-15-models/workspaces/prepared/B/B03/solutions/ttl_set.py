"""Implement the public contract from TASKS.md."""

import math


def _check_num(value, name):
    """Validate that *value* is a finite int or float that is not bool."""
    if isinstance(value, bool):
        raise TypeError(f"{name} must not be bool")
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be int or float, got {type(value).__name__}")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


class BoundedTTLSet:
    """A bounded set whose entries expire after a per-item time-to-live.

    Uses a plain list of ``(value, deadline)`` pairs so that unhashable
    (but equality-comparable) objects are supported.
    """

    def __init__(self, capacity, ttl, clock):
        _check_num(capacity, "capacity")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if not isinstance(capacity, int):
            raise TypeError("capacity must be int")

        _check_num(ttl, "ttl")
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")

        if not callable(clock):
            raise TypeError("clock must be callable")

        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._entries = []  # list of [value, deadline] — insertion order

    def _now(self):
        value = self._clock()
        _check_num(value, "clock() result")
        return value

    def _purge(self):
        """Remove all expired entries.  Called before every observable operation."""
        now = self._now()
        self._entries = [e for e in self._entries if now < e[1]]

    def add(self, value):
        self._purge()
        # Remove any *equal* existing entry (frees old object reference and
        # resets insertion position).  Check equality in both directions to
        # handle asymmetric ``__eq__`` implementations.
        for i, (v, _deadline) in enumerate(self._entries):
            if v == value or value == v:
                self._entries.pop(i)
                break
        now = self._now()
        self._entries.append([value, now + self._ttl])
        # Evict oldest (first in list) if over capacity
        if len(self._entries) > self._capacity:
            self._entries.pop(0)

    def discard(self, value):
        self._purge()
        for i, (v, _deadline) in enumerate(self._entries):
            if v == value or value == v:
                self._entries.pop(i)
                return

    def __contains__(self, value):
        self._purge()
        for v, _deadline in self._entries:
            if v == value or value == v:
                return True
        return False

    def __len__(self):
        self._purge()
        return len(self._entries)
