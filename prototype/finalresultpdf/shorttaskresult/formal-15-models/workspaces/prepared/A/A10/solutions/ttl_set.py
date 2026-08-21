"""Implement the public contract from TASKS.md."""


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        # Validate parameters
        assert isinstance(capacity, int) and not isinstance(capacity, bool)
        assert capacity > 0
        assert isinstance(ttl, (int, float)) and not isinstance(ttl, bool)
        assert ttl >= 0
        assert callable(clock)
        
        self.capacity = capacity
        self.ttl = ttl
        self.clock = clock
        
        # Internal storage: value -> (deadline, insertion order)
        self._data = {}
        # Insertion order tracking
        self._insertion_order = []
        self._next_order = 0
    
    def _purge_expired(self):
        now = self.clock()
        # Validate clock result
        assert isinstance(now, (int, float)) and not isinstance(now, bool)
        assert float('-inf') < now < float('inf')
        
        # Find expired entries
        expired = []
        for value, (deadline, _) in self._data.items():
            if now >= deadline:
                expired.append(value)
        
        # Remove expired entries
        for value in expired:
            self.discard(value)
    
    def add(self, value):
        self._purge_expired()
        
        # If value exists, replace it
        if value in self._data:
            self.discard(value)
        
        # If at capacity, evict oldest live entry
        if len(self._data) >= self.capacity:
            # Find oldest entry by insertion order
            oldest_value = min(self._data.keys(), key=lambda v: self._data[v][1])
            self.discard(oldest_value)
        
        # Add new entry
        now = self.clock()
        deadline = now + self.ttl
        self._data[value] = (deadline, self._next_order)
        self._insertion_order.append((self._next_order, value))
        self._next_order += 1
    
    def discard(self, value):
        if value in self._data:
            del self._data[value]
            # Note: We don't remove from _insertion_order to avoid O(n) scan;
            # it will be cleaned up when the order number is encountered again
    
    def __contains__(self, value):
        self._purge_expired()
        return value in self._data
    
    def __len__(self):
        self._purge_expired()
        return len(self._data)
