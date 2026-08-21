"""Implement the public contract from TASKS.md."""
import math
from collections import OrderedDict


def _check_numeric(value, name):
    if type(value) is bool:
        raise TypeError(f"{name} must not be bool")
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be int or float")
    if not math.isfinite(value):
        raise ValueError(f"{name} must be finite")


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        # Validate parameters
        if type(capacity) is bool or not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("capacity must be a positive int (not bool)")
        _check_numeric(ttl, "ttl")
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")
        if not callable(clock):
            raise TypeError("clock must be callable")
        
        self.capacity = capacity
        self.ttl = ttl
        self.clock = clock
        self._storage = OrderedDict()

    def _purge(self, now):
        # Purge all expired entries (must scan all, no assumption about clock monotonicity)
        expired = []
        for key, deadline in self._storage.items():
            if now >= deadline:
                expired.append(key)
        for key in expired:
            del self._storage[key]

    def _get_now(self):
        now = self.clock()
        _check_numeric(now, "clock result")
        return now

    def add(self, value):
        now = self._get_now()
        self._purge(now)
        
        # If exists, delete first to replace key object, deadline, and position
        if value in self._storage:
            del self._storage[value]
        
        # Add new entry
        deadline = now + self.ttl
        self._storage[value] = deadline
        
        # Enforce capacity
        if len(self._storage) > self.capacity:
            self._storage.popitem(last=False)

    def discard(self, value):
        now = self._get_now()
        self._purge(now)
        
        if value in self._storage:
            del self._storage[value]

    def __contains__(self, value):
        now = self._get_now()
        self._purge(now)
        return value in self._storage

    def __len__(self):
        now = self._get_now()
        self._purge(now)
        return len(self._storage)
