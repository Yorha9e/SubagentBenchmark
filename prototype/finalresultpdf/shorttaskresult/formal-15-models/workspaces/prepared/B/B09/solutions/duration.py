"""Implement the public contract from TASKS.md."""


class DurationParseError(ValueError):
    def __init__(self, code, position):
        self.code = code
        self.position = position
        super().__init__(f"Duration parse error: {code} at position {position}")


_UNITS = [
    ('ms', 'milliseconds', 1),
    ('s', 'seconds', 1000),
    ('m', 'minutes', 60 * 1000),
    ('h', 'hours', 60 * 60 * 1000),
    ('d', 'days', 24 * 60 * 60 * 1000),
]
_UNIT_RANKS = {u: len(_UNITS) - 1 - i for i, (u, _, _) in enumerate(_UNITS)}
_OUTPUT_KEYS = ['days', 'hours', 'minutes', 'seconds', 'milliseconds']
_PARSE_LIMITS = {'hours': 24, 'minutes': 60, 'seconds': 60, 'milliseconds': 1000}


def _scan_fields(text):
    if not isinstance(text, str):
        raise DurationParseError('type', 0)
    
    if len(text) == 0:
        raise DurationParseError('empty', 0)
    
    pos = 0
    fields = []
    last_rank = -1
    
    while pos < len(text):
        if not ('0' <= text[pos] <= '9'):
            raise DurationParseError('syntax', pos)
        
        num_start = pos
        while pos < len(text) and '0' <= text[pos] <= '9':
            pos += 1
        
        num_str = text[num_start:pos]
        if len(num_str) > 1 and num_str[0] == '0':
            raise DurationParseError('leading_zero', num_start)
        value = int(num_str)
        
        if pos >= len(text):
            raise DurationParseError('syntax', pos)
        
        unit_start = pos
        if pos + 1 < len(text) and text[pos:pos + 2] == 'ms':
            unit = 'ms'
            pos += 2
        else:
            unit = text[pos]
            pos += 1
        
        if unit not in _UNIT_RANKS:
            raise DurationParseError('syntax', unit_start)
        
        rank = _UNIT_RANKS[unit]
        if rank <= last_rank:
            raise DurationParseError('order', unit_start)
        last_rank = rank
        
        fields.append((value, unit, num_start))
    
    return fields


def parse_duration(text):
    fields = _scan_fields(text)
    result = {key: 0 for key in _OUTPUT_KEYS}
    
    value_map = {
        'd': 'days',
        'h': 'hours',
        'm': 'minutes',
        's': 'seconds',
        'ms': 'milliseconds'
    }
    
    for value, unit, num_start in fields:
        key = value_map[unit]
        limit = _PARSE_LIMITS.get(key)
        if limit is not None and value >= limit:
            raise DurationParseError('range', num_start)
        result[key] = value
    
    return result


def normalize_duration(text):
    fields = _scan_fields(text)
    
    total_ms = 0
    for value, unit, _ in fields:
        for u, _, ms in _UNITS:
            if u == unit:
                total_ms += value * ms
                break
    
    if total_ms == 0:
        return '0s'
    
    remaining = total_ms
    parts = []
    
    for unit, _, ms in reversed(_UNITS):
        if remaining >= ms:
            count = remaining // ms
            parts.append(f"{count}{unit}")
            remaining = remaining % ms
    
    return ''.join(parts)
