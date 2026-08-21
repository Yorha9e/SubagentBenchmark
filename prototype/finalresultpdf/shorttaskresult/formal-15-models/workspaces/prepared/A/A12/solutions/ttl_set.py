"""Bounded set with per-entry time-to-live and capacity eviction."""


class BoundedTTLSet:
    """A bounded set where entries expire after *ttl* units and the oldest
    live insertion is evicted when *capacity* is exceeded.

    *clock* is a callable returning the current time as a finite
    ``int`` or ``float`` (not ``bool``).
    """

    def __init__(self, capacity, ttl, clock):
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError("capacity must be an int (not bool)")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        if isinstance(ttl, bool) or not isinstance(ttl, (int, float)):
            raise TypeError("ttl must be int or float")
        if ttl != ttl or ttl == float("inf") or ttl == float("-inf"):
            raise ValueError("ttl must be finite")
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")
        if not callable(clock):
            raise TypeError("clock must be callable")

        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._data = {}   # value -> deadline
        self._order = []   # insertion-ordered list of live values

    # -- internal helpers --------------------------------------------------

    def _now(self):
        """Get validated current time from the clock."""
        t = self._clock()
        if isinstance(t, bool) or not isinstance(t, (int, float)):
            raise TypeError("clock must return int or float")
        if t != t or t == float("inf") or t == float("-inf"):
            raise ValueError("clock must return a finite value")
        return t

    def _purge(self):
        """Remove all entries whose deadline has been reached."""
        now = self._now()
        expired = [v for v, d in self._data.items() if now >= d]
        for v in expired:
            del self._data[v]
            self._order.remove(v)

    # -- public API --------------------------------------------------------

    def add(self, value):
        self._purge()
        deadline = self._now() + self._ttl
        if value in self._data:
            # Replace existing: update deadline and move to newest position.
            self._order.remove(value)
        elif len(self._data) >= self._capacity:
            # Evict oldest live insertion.
            oldest = self._order.pop(0)
            del self._data[oldest]
        self._data[value] = deadline
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
