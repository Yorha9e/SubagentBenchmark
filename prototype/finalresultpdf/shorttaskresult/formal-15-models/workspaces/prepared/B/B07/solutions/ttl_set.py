"""A bounded set whose entries expire after a fixed time-to-live."""

from collections import OrderedDict
import math


def _validate_number(value, name):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be an int or float")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    return value


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        if isinstance(capacity, bool) or not isinstance(capacity, int):
            raise TypeError("capacity must be an int")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        ttl = _validate_number(ttl, "ttl")
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")
        if not callable(clock):
            raise TypeError("clock must be callable")

        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._entries = OrderedDict()

    def _now(self):
        return _validate_number(self._clock(), "clock result")

    def _purge(self, now):
        for value, deadline in list(self._entries.items()):
            if now >= deadline:
                del self._entries[value]

    def _deadline(self, now):
        try:
            return now + self._ttl
        except OverflowError:
            return math.inf

    def add(self, value):
        now = self._now()
        self._purge(now)

        if value in self._entries:
            del self._entries[value]
        self._entries[value] = self._deadline(now)

        while len(self._entries) > self._capacity:
            self._entries.popitem(last=False)

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
