"""Implement the public contract from TASKS.md."""


class DurationParseError(ValueError):
    def __init__(self, code, position):
        self.code = code
        self.position = position
        super().__init__(f"Error {code} at position {position}")


# Fixed metadata
_UNIT_RANKS = {
    'd': 0,
    'h': 1,
    'm': 2,
    's': 3,
    'ms': 4
}
_UNIT_NAMES = ['d', 'h', 'm', 's', 'ms']
_OUTPUT_KEYS = ['days', 'hours', 'minutes', 'seconds', 'milliseconds']
_PARSE_RANGES = {
    'h': 24,
    'm': 60,
    's': 60,
    'ms': 1000
}


def _scan(text):
    if not isinstance(text, str):
        raise DurationParseError('type', 0)
    if len(text) == 0:
        raise DurationParseError('empty', 0)
    
    fields = []
    pos = 0
    n = len(text)
    last_rank = -1
    
    while pos < n:
        # Read digits
        digit_start = pos
        while pos < n and '0' <= text[pos] <= '9':
            pos += 1
        if pos == digit_start:
            # No digits, syntax error
            raise DurationParseError('syntax', pos)
        
        # Check leading zero
        digits = text[digit_start:pos]
        if len(digits) > 1 and digits[0] == '0':
            raise DurationParseError('leading_zero', digit_start)
        value = int(digits)
        
        # Read unit
        unit_start = pos
        # Try 'ms' first
        if pos + 1 < n and text[pos:pos+2] == 'ms':
            unit = 'ms'
            pos += 2
        elif pos < n and text[pos] in 'dhms':
            unit = text[pos]
            pos += 1
        else:
            # Invalid unit
            raise DurationParseError('syntax', unit_start)
        
        # Check rank order
        rank = _UNIT_RANKS[unit]
        if rank <= last_rank:
            raise DurationParseError('order', unit_start)
        last_rank = rank
        
        fields.append((unit, value, digit_start, unit_start))
    
    return fields


def parse_duration(text):
    fields = _scan(text)
    
    # Initialize result dict
    result = {key: 0 for key in _OUTPUT_KEYS}
    
    # Check ranges
    for unit, value, digit_start, _ in fields:
        if unit == 'd':
            result['days'] = value
        elif unit == 'h':
            if value >= _PARSE_RANGES['h']:
                raise DurationParseError('range', digit_start)
            result['hours'] = value
        elif unit == 'm':
            if value >= _PARSE_RANGES['m']:
                raise DurationParseError('range', digit_start)
            result['minutes'] = value
        elif unit == 's':
            if value >= _PARSE_RANGES['s']:
                raise DurationParseError('range', digit_start)
            result['seconds'] = value
        elif unit == 'ms':
            if value >= _PARSE_RANGES['ms']:
                raise DurationParseError('range', digit_start)
            result['milliseconds'] = value
    
    return result


def normalize_duration(text):
    fields = _scan(text)
    
    # Convert all to milliseconds
    total_ms = 0
    for unit, value, _, _ in fields:
        if unit == 'd':
            total_ms += value * 24 * 60 * 60 * 1000
        elif unit == 'h':
            total_ms += value * 60 * 60 * 1000
        elif unit == 'm':
            total_ms += value * 60 * 1000
        elif unit == 's':
            total_ms += value * 1000
        elif unit == 'ms':
            total_ms += value
    
    # Handle zero case
    if total_ms == 0:
        return '0s'
    
    # Break down into canonical form
    remaining = total_ms
    days, remaining = divmod(remaining, 24 * 60 * 60 * 1000)
    hours, remaining = divmod(remaining, 60 * 60 * 1000)
    minutes, remaining = divmod(remaining, 60 * 1000)
    seconds, milliseconds = divmod(remaining, 1000)
    
    # Build string parts, omitting zeros
    parts = []
    if days > 0:
        parts.append(f"{days}d")
    if hours > 0:
        parts.append(f"{hours}h")
    if minutes > 0:
        parts.append(f"{minutes}m")
    if seconds > 0:
        parts.append(f"{seconds}s")
    if milliseconds > 0:
        parts.append(f"{milliseconds}ms")
    
    return ''.join(parts)
