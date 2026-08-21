"""Implement the public contract from TASKS.md."""


class DurationParseError(ValueError):
    def __init__(self, code, position):
        self.code = code
        self.position = position
        super().__init__(f"{code} at position {position}")


# Unit definitions in descending order
UNITS = [
    ('ms', 'milliseconds', 1000),
    ('s', 'seconds', 60),
    ('m', 'minutes', 60),
    ('h', 'hours', 24),
    ('d', 'days', None),  # days have no limit
]

# Reverse order for parsing (descending priority)
UNIT_ORDER = ['d', 'h', 'm', 's', 'ms']
UNIT_TO_KEY = {
    'd': 'days',
    'h': 'hours',
    'm': 'minutes',
    's': 'seconds',
    'ms': 'milliseconds'
}


def _parse_field(text, start_pos):
    """Parse a single field starting at start_pos.
    Returns (value, unit, end_pos) or raises DurationParseError.
    """
    pos = start_pos
    n = len(text)
    
    # Parse digits
    digits = []
    while pos < n and text[pos].isdigit():
        digits.append(text[pos])
        pos += 1
    
    if not digits:
        raise DurationParseError('syntax', start_pos)
    
    # Check leading zero (except for single '0')
    digit_str = ''.join(digits)
    if len(digit_str) > 1 and digit_str[0] == '0':
        raise DurationParseError('leading_zero', start_pos)
    
    value = int(digit_str)
    
    # Parse unit
    unit_start = pos
    if pos + 1 < n and text[pos:pos+2] == 'ms':
        unit = 'ms'
        pos += 2
    elif pos < n and text[pos] in 'dhms':
        unit = text[pos]
        pos += 1
    else:
        raise DurationParseError('syntax', unit_start)
    
    return value, unit, pos


def parse_duration(text):
    # Check type
    if not isinstance(text, str):
        raise DurationParseError('type', 0)
    
    # Check empty
    if not text:
        raise DurationParseError('empty', 0)
    
    n = len(text)
    pos = 0
    parsed = {}
    last_unit_index = -1
    
    while pos < n:
        value, unit, new_pos = _parse_field(text, pos)
        
        # Check unit order
        try:
            unit_index = UNIT_ORDER.index(unit)
        except ValueError:
            raise DurationParseError('syntax', pos + len(str(value)))
        
        if unit_index <= last_unit_index:
            raise DurationParseError('order', pos + len(str(value)))
        last_unit_index = unit_index
        
        # Check for duplicate units
        if unit in parsed:
            raise DurationParseError('order', pos + len(str(value)))
        
        parsed[unit] = value
        pos = new_pos
    
    # Check range for subordinate units
    for unit in ['h', 'm', 's', 'ms']:
        if unit in parsed:
            value = parsed[unit]
            limit = None
            if unit == 'h':
                limit = 24
            elif unit in ['m', 's']:
                limit = 60
            elif unit == 'ms':
                limit = 1000
            
            if value >= limit:
                # Find position in text for this unit
                # This is a simplification - we don't track exact position
                raise DurationParseError('range', 0)
    
    # Build result dictionary with fixed key order
    result = {}
    for unit in UNIT_ORDER:
        key = UNIT_TO_KEY[unit]
        result[key] = parsed.get(unit, 0)
    
    return result


def normalize_duration(text):
    # Check type
    if not isinstance(text, str):
        raise DurationParseError('type', 0)
    
    # Check empty
    if not text:
        raise DurationParseError('empty', 0)
    
    n = len(text)
    pos = 0
    parsed = {}
    last_unit_index = -1
    
    while pos < n:
        value, unit, new_pos = _parse_field(text, pos)
        
        # Check unit order
        try:
            unit_index = UNIT_ORDER.index(unit)
        except ValueError:
            raise DurationParseError('syntax', pos + len(str(value)))
        
        if unit_index <= last_unit_index:
            raise DurationParseError('order', pos + len(str(value)))
        last_unit_index = unit_index
        
        # Check for duplicate units
        if unit in parsed:
            raise DurationParseError('order', pos + len(str(value)))
        
        parsed[unit] = value
        pos = new_pos
    
    # Convert all to milliseconds for normalization
    ms = 0
    if 'd' in parsed:
        ms += parsed['d'] * 24 * 60 * 60 * 1000
    if 'h' in parsed:
        ms += parsed['h'] * 60 * 60 * 1000
    if 'm' in parsed:
        ms += parsed['m'] * 60 * 1000
    if 's' in parsed:
        ms += parsed['s'] * 1000
    if 'ms' in parsed:
        ms += parsed['ms']
    
    # Handle zero case
    if ms == 0:
        return "0s"
    
    # Normalize from largest to smallest unit
    days = ms // (24 * 60 * 60 * 1000)
    ms %= (24 * 60 * 60 * 1000)
    
    hours = ms // (60 * 60 * 1000)
    ms %= (60 * 60 * 1000)
    
    minutes = ms // (60 * 1000)
    ms %= (60 * 1000)
    
    seconds = ms // 1000
    ms %= 1000
    
    milliseconds = ms
    
    # Build result string, omitting zeros
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
