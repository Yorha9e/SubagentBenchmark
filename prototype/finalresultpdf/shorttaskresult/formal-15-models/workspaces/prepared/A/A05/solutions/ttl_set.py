"""Implement the public contract from TASKS.md."""


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        if type(capacity) is not int or isinstance(capacity, bool) or capacity <= 0:
            raise TypeError("capacity must be a positive int")
        if not isinstance(ttl, (int, float)) or isinstance(ttl, bool) or ttl < 0:
            raise TypeError("ttl must be a non-negative finite number")
        if not callable(clock):
            raise TypeError("clock must be callable")
        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._map = {}       # value -> (deadline, order)
        self._order = []     # values in insertion order
        self._next_order = 0

    def _now(self):
        now = self._clock()
        if not isinstance(now, (int, float)) or isinstance(now, bool):
            raise TypeError("clock must return a finite number")
        return now

    def _purge(self):
        now = self._now()
        new_order = []
        for val in self._order:
            deadline, _ = self._map[val]
            if now >= deadline:
                del self._map[val]
            else:
                new_order.append(val)
        self._order = new_order

    def add(self, value):
        self._purge()
        now = self._now()
        deadline = now + self._ttl
        if value in self._map:
            self._order.remove(value)
            self._map[value] = (deadline, self._next_order)
            self._next_order += 1
            self._order.append(value)
        else:
            if len(self._order) >= self._capacity:
                oldest = self._order.pop(0)
                del self._map[oldest]
            self._map[value] = (deadline, self._next_order)
            self._next_order += 1
            self._order.append(value)

    def discard(self, value):
        self._purge()
        if value in self._map:
            self._order.remove(value)
            del self._map[value]

    def __contains__(self, value):
        self._purge()
        return value in self._map

    def __len__(self):
        self._purge()
        return len(self._map)
