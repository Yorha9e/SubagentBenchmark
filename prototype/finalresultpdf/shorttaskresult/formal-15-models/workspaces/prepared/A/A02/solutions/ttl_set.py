"""Implement the public contract from TASKS.md."""


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        if isinstance(capacity, bool) or type(capacity) is not int:
            raise TypeError("capacity must be a non-bool int")
        if capacity <= 0:
            raise ValueError("capacity must be positive")

        if isinstance(ttl, bool) or not isinstance(ttl, (int, float)):
            raise TypeError("ttl must be a non-bool int or float")

        if not callable(clock):
            raise TypeError("clock must be callable")

        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock

        # Ordered by insertion: value -> (deadline, insert_order)
        self._data = {}
        self._counter = 0

    def _purge(self):
        now = self._clock()
        expired = [k for k, (deadline, _) in self._data.items() if now >= deadline]
        for k in expired:
            del self._data[k]

    def add(self, value):
        self._purge()
        now = self._clock()
        deadline = now + self._ttl

        if value in self._data:
            # Replace existing: update deadline and make newest
            self._counter += 1
            self._data[value] = (deadline, self._counter)
        else:
            if len(self._data) >= self._capacity:
                # Evict oldest live insertion
                oldest = min(self._data.items(), key=lambda kv: kv[1][1])[0]
                del self._data[oldest]

            self._counter += 1
            self._data[value] = (deadline, self._counter)

    def discard(self, value):
        self._purge()
        self._data.pop(value, None)

    def __contains__(self, value):
        self._purge()
        return value in self._data

    def __len__(self):
        self._purge()
        return len(self._data)
