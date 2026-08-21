"""Implement the public contract from TASKS.md."""
import math
from collections import OrderedDict


def _validate_numeric(value, allow_negative=True):
    """Validate that value is a finite int/float but not bool."""
    if isinstance(value, bool):
        raise TypeError("value must not be bool")
    if not isinstance(value, (int, float)):
        raise TypeError("value must be int or float")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("value must be finite")
    if not allow_negative and value < 0:
        raise ValueError("value must be nonnegative")


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        # Validate capacity
        if isinstance(capacity, bool):
            raise TypeError("capacity must not be bool")
        if not isinstance(capacity, int):
            raise TypeError("capacity must be int")
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        # Validate ttl
        _validate_numeric(ttl, allow_negative=False)

        # Validate clock is callable
        if not callable(clock):
            raise TypeError("clock must be callable")

        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._items = OrderedDict()  # key -> deadline

    def _purge(self, now):
        """Remove all expired entries. Must scan all entries for non-monotonic clock."""
        expired_keys = [key for key, deadline in self._items.items() if now >= deadline]
        for key in expired_keys:
            del self._items[key]

    def _get_now(self):
        now = self._clock()
        _validate_numeric(now, allow_negative=True)
        return now

    def add(self, value):
        now = self._get_now()
        self._purge(now)

        # If key already exists (by equality), remove old entry first
        # to replace the stored object, deadline, and insertion position
        if value in self._items:
            del self._items[value]

        deadline = now + self._ttl
        self._items[value] = deadline

        # Capacity eviction: remove oldest live insertion
        while len(self._items) > self._capacity:
            self._items.popitem(last=False)

    def discard(self, value):
        now = self._get_now()
        self._purge(now)

        if value in self._items:
            del self._items[value]

    def __contains__(self, value):
        now = self._get_now()
        self._purge(now)
        return value in self._items

    def __len__(self):
        now = self._get_now()
        self._purge(now)
        return len(self._items)
