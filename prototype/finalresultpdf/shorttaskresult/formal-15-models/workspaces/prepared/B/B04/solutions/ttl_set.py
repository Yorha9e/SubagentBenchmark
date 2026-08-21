"""Implement the public contract from TASKS.md."""

import math
from collections import OrderedDict


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        self._capacity = self._validate_positive_int(capacity, "capacity")
        self._ttl = self._validate_finite_nonnegative_number(ttl, "ttl")
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._clock = clock
        self._data = OrderedDict()  # value -> deadline

    @staticmethod
    def _validate_positive_int(value, name):
        if isinstance(value, bool) or not isinstance(value, int):
            raise TypeError(f"{name} must be an int")
        if value <= 0:
            raise ValueError(f"{name} must be positive")
        return value

    @staticmethod
    def _validate_finite_number(value, name):
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise TypeError(f"{name} must be an int or float")
        if isinstance(value, float) and not math.isfinite(value):
            raise ValueError(f"{name} must be finite")
        return value

    @staticmethod
    def _validate_finite_nonnegative_number(value, name):
        value = BoundedTTLSet._validate_finite_number(value, name)
        if value < 0:
            raise ValueError(f"{name} must be nonnegative")
        return value

    def _now(self):
        now = self._clock()
        return self._validate_finite_number(now, "clock")

    def _purge(self, now):
        expired_keys = [key for key, deadline in self._data.items() if now >= deadline]
        for key in expired_keys:
            del self._data[key]

    def add(self, value):
        now = self._now()
        self._purge(now)

        if value in self._data:
            del self._data[value]

        self._data[value] = now + self._ttl

        while len(self._data) > self._capacity:
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
