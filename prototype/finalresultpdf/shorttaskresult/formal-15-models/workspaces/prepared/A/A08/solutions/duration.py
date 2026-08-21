"""Implement the public contract from TASKS.md."""

# Unit rank: lower number = larger unit (descending order d, h, m, s, ms)
_UNIT_RANK = {'d': 0, 'h': 1, 'm': 2, 's': 3, 'ms': 4}
_UNIT_KEYS = {0: 'days', 1: 'hours', 2: 'minutes', 3: 'seconds', 4: 'milliseconds'}
_UNIT_LABELS = {0: 'd', 1: 'h', 2: 'm', 3: 's', 4: 'ms'}
# Range limits for parse_duration (subordinate units)
_RANGE_LIMITS = {1: 24, 2: 60, 3: 60, 4: 1000}  # h<24, m<60, s<60, ms<1000
# Conversion: milliseconds per unit
_MS_PER_UNIT = {0: 86400000, 1: 3600000, 2: 60000, 3: 1000, 4: 1}


class DurationParseError(ValueError):
    def __init__(self, code, position):
        self.code = code
        self.position = position
        super().__init__(f"{code} at position {position}")


def _parse_fields(text):
    """
    Parse duration text into list of (rank, value, value_start_pos).
    Raises DurationParseError for type, empty, syntax, leading_zero, order errors.
    Does NOT check range limits.
    """
    # Type check
    if not isinstance(text, str):
        raise DurationParseError('type', 0)

    # Empty check
    if len(text) == 0:
        raise DurationParseError('empty', 0)

    fields = []
    pos = 0
    last_rank = -1  # sentinel: first valid unit always has rank >= 0

    while pos < len(text):
        # Parse digits
        value_start = pos
        while pos < len(text) and text[pos].isdigit():
            pos += 1

        if pos == value_start:
            # Expected digits but found something else
            raise DurationParseError('syntax', pos)

        num_str = text[value_start:pos]

        # Leading zero check: more than one digit starting with '0'
        if len(num_str) > 1 and num_str[0] == '0':
            raise DurationParseError('leading_zero', value_start)

        value = int(num_str)

        # Parse unit: try 2-char unit ("ms") first
        unit = None
        unit_len = 0
        unit_start = pos
        if pos + 1 < len(text) and text[pos:pos + 2] == 'ms':
            unit = 'ms'
            unit_len = 2
        elif pos < len(text) and text[pos] in ('d', 'h', 'm', 's'):
            unit = text[pos]
            unit_len = 1
        else:
            raise DurationParseError('syntax', pos)

        rank = _UNIT_RANK[unit]

        # Order check: must be strictly descending (rank strictly increasing)
        if rank <= last_rank:
            raise DurationParseError('order', unit_start)

        last_rank = rank
        pos += unit_len
        fields.append((rank, value, value_start))

    return fields


def parse_duration(text):
    fields = _parse_fields(text)

    # Build result dict with all keys in fixed order
    result = {
        'days': 0,
        'hours': 0,
        'minutes': 0,
        'seconds': 0,
        'milliseconds': 0,
    }

    # Validate ranges for subordinate units
    for rank, value, value_start in fields:
        if rank in _RANGE_LIMITS:
            limit = _RANGE_LIMITS[rank]
            if value >= limit:
                raise DurationParseError('range', value_start)
        result[_UNIT_KEYS[rank]] = value

    return result


def normalize_duration(text):
    fields = _parse_fields(text)

    # Compute total milliseconds
    total_ms = 0
    for rank, value, _ in fields:
        total_ms += value * _MS_PER_UNIT[rank]

    # Canonical zero is "0s"
    if total_ms == 0:
        return "0s"

    # Decompose into largest units first (shortest canonical equivalent)
    parts = []
    remaining = total_ms
    for rank in range(5):  # 0=d, 1=h, 2=m, 3=s, 4=ms
        unit_ms = _MS_PER_UNIT[rank]
        amount = remaining // unit_ms
        remaining = remaining % unit_ms
        if amount > 0:
            parts.append(f"{amount}{_UNIT_LABELS[rank]}")

    return ''.join(parts)
