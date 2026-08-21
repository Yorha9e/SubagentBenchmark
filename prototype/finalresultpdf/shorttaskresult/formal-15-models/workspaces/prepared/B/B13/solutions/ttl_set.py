"""Implement the public contract from TASKS.md."""

import math
from collections import OrderedDict


def _validate_numeric(value, name, allow_zero=True):
    """Validate that value is a finite int/float but not bool."""
    if type(value) is bool:
        raise TypeError(f"{name} must be an int or float, not bool")
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be an int or float, got {type(value).__name__}")
    if isinstance(value, float) and (math.isinf(value) or math.isnan(value)):
        raise ValueError(f"{name} must be finite, got {value}")
    if not allow_zero and value <= 0:
        raise ValueError(f"{name} must be positive, got {value}")
    if allow_zero and value < 0:
        raise ValueError(f"{name} must be nonnegative, got {value}")


class BoundedTTLSet:
    """A set with bounded capacity and per-entry TTL expiration."""

    def __init__(self, capacity, ttl, clock):
        if type(capacity) is bool or not isinstance(capacity, int):
            raise TypeError(f"capacity must be an int (not bool), got {type(capacity).__name__}")
        if capacity <= 0:
            raise ValueError(f"capacity must be positive, got {capacity}")
        _validate_numeric(ttl, "ttl")
        if not callable(clock):
            raise TypeError("clock must be callable")

        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        # OrderedDict: key -> deadline; insertion order = oldest-first
        self._data = OrderedDict()

    def _purge_expired(self, now):
        """Remove all entries where clock() >= deadline."""
        # Must scan all entries (non-monotonic clock)
        expired_keys = [k for k, deadline in self._data.items() if now >= deadline]
        for k in expired_keys:
            del self._data[k]

    def _get_now(self):
        """Get and validate current time from clock."""
        now = self._clock()
        _validate_numeric(now, "clock result")
        return now

    def add(self, value):
        now = self._get_now()
        self._purge_expired(now)

        # Check if value already exists (by equality)
        existing_key = None
        for k in self._data:
            if k == value:
                existing_key = k
                break

        if existing_key is not None:
            # Remove old entry (don't keep stale reference)
            del self._data[existing_key]

        # Add new entry at end (most recently inserted)
        deadline = now + self._ttl
        self._data[value] = deadline

        # Evict oldest if over capacity
        while len(self._data) > self._capacity:
            self._data.popitem(last=False)

    def discard(self, value):
        now = self._get_now()
        self._purge_expired(now)

        # Remove if exists
        keys_to_remove = [k for k in self._data if k == value]
        for k in keys_to_remove:
            del self._data[k]

    def __contains__(self, value):
        now = self._get_now()
        self._purge_expired(now)
        return any(k == value for k in self._data)

    def __len__(self):
        now = self._get_now()
        self._purge_expired(now)
        return len(self._data)
