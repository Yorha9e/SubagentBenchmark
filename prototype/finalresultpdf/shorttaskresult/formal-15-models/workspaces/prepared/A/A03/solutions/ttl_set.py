"""Implement the public contract from TASKS.md."""

import math


class BoundedTTLSet:
    """A bounded set with per-entry TTL-based expiration and capacity eviction."""

    def __init__(self, capacity, ttl, clock):
        if isinstance(capacity, bool) or type(capacity) is not int:
            raise TypeError("capacity must be an int")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if isinstance(ttl, bool) or not isinstance(ttl, (int, float)):
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
        # Ordered dict: value -> deadline.  Insertion order is preserved;
        # replacement re-inserts to reset the position.
        self._data = {}

    def _purge(self):
        """Remove all expired entries."""
        now = self._clock()
        expired = [v for v, deadline in self._data.items() if deadline <= now]
        for v in expired:
            del self._data[v]

    def add(self, value):
        """Add *value* (replacing an equal existing entry), evicting if needed."""
        self._purge()
        if value in self._data:
            # Remove so the re-insert updates the insertion position and
            # replaces the stored object reference.
            del self._data[value]
        elif len(self._data) >= self._capacity:
            # Evict the oldest live entry (first key in insertion order).
            oldest = next(iter(self._data))
            del self._data[oldest]
        self._data[value] = self._clock() + self._ttl

    def discard(self, value):
        """Remove *value* if present."""
        self._purge()
        self._data.pop(value, None)

    def __contains__(self, value):
        """Return True when *value* is present and not expired."""
        self._purge()
        return value in self._data

    def __len__(self):
        """Return the number of live (non-expired) entries."""
        self._purge()
        return len(self._data)
