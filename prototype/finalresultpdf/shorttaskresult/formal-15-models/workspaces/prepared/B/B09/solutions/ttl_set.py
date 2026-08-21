"""Implement the public contract from TASKS.md."""
import math
from collections import OrderedDict


def _validate_numeric(value, name, allow_zero=True, non_negative=True):
    if type(value) is bool:
        raise TypeError(f"{name} must not be bool")
    if not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be int or float")
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError(f"{name} must be finite")
    if non_negative and value < 0:
        raise ValueError(f"{name} must be non-negative")
    if not allow_zero and value <= 0:
        raise ValueError(f"{name} must be positive")


class BoundedTTLSet:
    def __init__(self, capacity, ttl, clock):
        _validate_numeric(capacity, "capacity", allow_zero=False)
        _validate_numeric(ttl, "ttl", allow_zero=True)
        if not callable(clock):
            raise TypeError("clock must be callable")
        
        self._capacity = capacity
        self._ttl = ttl
        self._clock = clock
        self._entries = OrderedDict()
    
    def _purge(self):
        now = self._clock()
        _validate_numeric(now, "clock value", allow_zero=True, non_negative=False)
        
        expired_keys = []
        for key, deadline in self._entries.items():
            if now >= deadline:
                expired_keys.append(key)
        
        for key in expired_keys:
            del self._entries[key]
        
        return now
    
    def add(self, value):
        now = self._purge()
        
        if value in self._entries:
            del self._entries[value]
        
        self._entries[value] = now + self._ttl
        
        while len(self._entries) > self._capacity:
            self._entries.popitem(last=False)
    
    def discard(self, value):
        self._purge()
        if value in self._entries:
            del self._entries[value]
    
    def __contains__(self, value):
        self._purge()
        return value in self._entries
    
    def __len__(self):
        self._purge()
        return len(self._entries)
