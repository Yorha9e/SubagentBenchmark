"""Implement the public contract from TASKS.md."""

import math


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        # Validate capacity
        if not isinstance(capacity, int) or isinstance(capacity, bool):
            raise TypeError("capacity must be an int but not bool")
        if capacity <= 0:
            raise ValueError("capacity must be positive")
        
        # Validate ttl
        if not (isinstance(ttl, (int, float)) and not isinstance(ttl, bool)):
            raise TypeError("ttl must be a finite int or float but not bool")
        if not math.isfinite(ttl):
            raise ValueError("ttl must be finite")
        if ttl < 0:
            raise ValueError("ttl must be nonnegative")
        
        # Validate clock is callable
        if not callable(clock):
            raise TypeError("clock must be callable")
        
        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        
        # Internal storage: {value: (deadline, insertion_order)}
        self._entries = {}
        self._insertion_counter = 0
    
    def _purge_expired(self):
        """Remove all expired entries before observable operations."""
        now = self._clock()
        # Validate clock result
        if not (isinstance(now, (int, float)) and not isinstance(now, bool)):
            raise TypeError("clock must return a finite int or float but not bool")
        if not math.isfinite(now):
            raise ValueError("clock result must be finite")
        
        # Find expired entries
        expired = [value for value, (deadline, _) in self._entries.items()
                   if now >= deadline]
        
        for value in expired:
            del self._entries[value]
    
    def _evict_if_needed(self):
        """Evict oldest live entry if at capacity."""
        if len(self._entries) >= self._capacity:
            # Find the oldest live entry (smallest insertion_order)
            oldest_value = min(self._entries.keys(),
                             key=lambda v: self._entries[v][1])
            del self._entries[oldest_value]
    
    def add(self, value):
        self._purge_expired()
        
        # If value already exists, remove it first to replace
        if value in self._entries:
            del self._entries[value]
        
        # Evict if at capacity before adding new entry
        self._evict_if_needed()
        
        # Calculate deadline
        now = self._clock()
        deadline = now + self._ttl
        
        # Store with insertion order
        self._insertion_counter += 1
        self._entries[value] = (deadline, self._insertion_counter)
    
    def discard(self, value):
        self._purge_expired()
        if value in self._entries:
            del self._entries[value]
    
    def __contains__(self, value):
        self._purge_expired()
        return value in self._entries
    
    def __len__(self):
        self._purge_expired()
        return len(self._entries)
