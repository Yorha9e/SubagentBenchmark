"""Implement the public contract from TASKS.md."""


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        if type(capacity) is not int:
            raise TypeError("capacity must be an int")
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        if type(ttl) is bool:
            raise TypeError("ttl must not be bool")
        if not isinstance(ttl, (int, float)):
            raise TypeError("ttl must be a number")
        if ttl != ttl or ttl == float("inf") or ttl == float("-inf"):
            raise ValueError("ttl must be finite")
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")

        if not callable(clock):
            raise TypeError("clock must be callable")

        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._data = {}
        self._order = []

    def _purge(self):
        now = self._clock()
        if type(now) is bool:
            raise TypeError("clock must not return bool")
        if not isinstance(now, (int, float)):
            raise TypeError("clock must return a number")
        if now != now or now == float("inf") or now == float("-inf"):
            raise ValueError("clock must return a finite number")
        expired = [v for v, d in self._data.items() if now >= d]
        for v in expired:
            del self._data[v]
        if expired:
            self._order = [v for v in self._order if v in self._data]

    def add(self, value):
        self._purge()
        existing = None
        for k in self._data:
            if k == value:
                existing = k
                break
        if existing is not None:
            self._order.remove(existing)
            del self._data[existing]
        elif len(self._data) >= self._capacity:
            oldest = self._order.pop(0)
            del self._data[oldest]
        self._data[value] = self._clock() + self._ttl
        self._order.append(value)

    def discard(self, value):
        self._purge()
        if value in self._data:
            del self._data[value]
            self._order.remove(value)

    def __contains__(self, value):
        self._purge()
        return value in self._data

    def __len__(self):
        self._purge()
        return len(self._data)
