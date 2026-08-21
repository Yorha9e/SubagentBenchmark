import math
import collections


def _is_finite_number(val):
    if isinstance(val, bool):
        return False
    if isinstance(val, (int, float)):
        return math.isfinite(val)
    return False


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        if not isinstance(capacity, int) or isinstance(capacity, bool) or capacity <= 0:
            raise ValueError("capacity must be a positive int")
        if not _is_finite_number(ttl) or ttl < 0:
            raise ValueError("ttl must be a non-negative finite number")
        if not callable(clock):
            raise ValueError("clock must be callable")

        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._data = collections.OrderedDict()

    def _purge(self):
        now = self._clock()
        if not _is_finite_number(now):
            raise ValueError("clock returned non-finite value")
        to_remove = []
        for key, deadline in self._data.items():
            if now >= deadline:
                to_remove.append(key)
        for key in to_remove:
            del self._data[key]

    def add(self, value):
        now = self._clock()
        if not _is_finite_number(now):
            raise ValueError("clock returned non-finite value")
        self._purge()

        if value in self._data:
            del self._data[value]

        self._data[value] = now + self._ttl

        while len(self._data) > self._capacity:
            self._data.popitem(last=False)

    def discard(self, value):
        now = self._clock()
        if not _is_finite_number(now):
            raise ValueError("clock returned non-finite value")
        self._purge()
        self._data.pop(value, None)

    def __contains__(self, value):
        now = self._clock()
        if not _is_finite_number(now):
            raise ValueError("clock returned non-finite value")
        self._purge()
        return value in self._data

    def __len__(self):
        now = self._clock()
        if not _is_finite_number(now):
            raise ValueError("clock returned non-finite value")
        self._purge()
        return len(self._data)
