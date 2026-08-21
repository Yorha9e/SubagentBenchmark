import math
from collections import OrderedDict


class BoundedTTLSet:
    """A bounded set whose entries expire after a time-to-live."""

    def __init__(self, capacity, ttl, clock):
        if type(capacity) is not int:
            raise TypeError("capacity must be int")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if type(ttl) not in (int, float):
            raise TypeError("ttl must be int or float")
        if not math.isfinite(ttl):
            raise ValueError("ttl must be finite")
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._od = OrderedDict()  # key -> (stored_object, deadline)

    # -- internal helpers ------------------------------------------------

    def _now(self):
        result = self._clock()
        if type(result) not in (int, float):
            raise TypeError("clock result must be int or float")
        if not math.isfinite(result):
            raise ValueError("clock result must be finite")
        return result

    def _purge(self, now):
        """Remove every entry whose deadline has been reached."""
        expired = [
            key for key, (_, deadline) in self._od.items()
            if now >= deadline
        ]
        for key in expired:
            del self._od[key]

    # -- public API ------------------------------------------------------

    def add(self, value):
        now = self._now()
        self._purge(now)
        deadline = now + self._ttl
        # Replacing an existing equal key: drop the old entry so no stale
        # object reference survives, then re-insert at the end (newest).
        if value in self._od:
            del self._od[value]
        self._od[value] = (value, deadline)
        if len(self._od) > self._capacity:
            self._od.popitem(last=False)

    def discard(self, value):
        now = self._now()
        self._purge(now)
        self._od.pop(value, None)

    def __contains__(self, value):
        now = self._now()
        self._purge(now)
        return value in self._od

    def __len__(self):
        now = self._now()
        self._purge(now)
        return len(self._od)
