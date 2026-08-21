"""Implement the public contract from TASKS.md."""
import math


def _check_numeric(value, name):
    """Validate that value is a finite int/float but not bool."""
    if isinstance(value, bool) or type(value) not in (int, float):
        raise TypeError(f"{name} must be int or float, not bool")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        # Validate capacity: int but not bool, positive
        if isinstance(capacity, bool) or type(capacity) is not int:
            raise TypeError("capacity must be int, not bool")
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        # Validate ttl: finite int/float but not bool, nonnegative
        _check_numeric(ttl, "ttl")
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")

        # Validate clock: callable
        if not callable(clock):
            raise TypeError("clock must be callable")

        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        # Dict maintains insertion order; value -> deadline
        self._entries = {}

    def _get_time(self):
        now = self._clock()
        _check_numeric(now, "clock result")
        return now

    def _purge_expired(self):
        now = self._get_time()
        # Collect expired keys first, then delete (avoid dict mutation during iteration)
        expired = [key for key, deadline in self._entries.items() if now >= deadline]
        for key in expired:
            del self._entries[key]

    def add(self, value):
        self._purge_expired()
        now = self._get_time()
        deadline = now + self._ttl

        if value in self._entries:
            # Replace: remove first to update insertion position, then re-add
            del self._entries[value]
            self._entries[value] = deadline
        else:
            # Evict oldest live insertion if at capacity
            if len(self._entries) >= self._capacity:
                oldest = next(iter(self._entries))
                del self._entries[oldest]
            self._entries[value] = deadline

    def discard(self, value):
        self._purge_expired()
        if value in self._entries:
            del self._entries[value]

    def __contains__(self, value):
        self._purge_expired()
        return value in self._entries

    def __len__(self):
        self._purge_expired()
        return len(self._entries)
