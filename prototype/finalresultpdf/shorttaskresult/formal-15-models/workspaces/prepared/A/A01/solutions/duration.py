"""Implement the public contract from TASKS.md."""


class DurationParseError(ValueError):
    def __init__(self, code, position):
        self.code = code
        self.position = position
        super().__init__(f"{code} at {position}")


# unit -> (dict_key, order, max_exclusive); order higher = larger unit;
# max_exclusive None means unbounded (days).
_UNITS = {
    'd': ('days', 4, None),
    'h': ('hours', 3, 24),
    'm': ('minutes', 2, 60),
    's': ('seconds', 1, 60),
    'ms': ('milliseconds', 0, 1000),
}
_ORDER_TO_UNIT = {4: 'd', 3: 'h', 2: 'm', 1: 's', 0: 'ms'}


def _tokenize(text):
    """Return list of (key, value, unit, position). Raises DurationParseError
    for type/empty/syntax/leading_zero/order problems."""
    pos = 0
    n = len(text)
    fields = []
    last_order = 5  # larger than any real unit
    while pos < n:
        if not text[pos].isdigit():
            raise DurationParseError('syntax', pos)
        start = pos
        if text[pos] == '0':
            if pos + 1 < n and text[pos + 1].isdigit():
                raise DurationParseError('leading_zero', start)
            val = 0
            pos += 1
        else:
            while pos < n and text[pos].isdigit():
                pos += 1
            val = int(text[start:pos])
        if pos >= n:
            raise DurationParseError('syntax', pos)
        if text[pos] == 'd':
            unit = 'd'
            pos += 1
        elif text[pos] == 'h':
            unit = 'h'
            pos += 1
        elif text[pos] == 'm':
            if pos + 1 < n and text[pos + 1] == 's':
                unit = 'ms'
                pos += 2
            else:
                unit = 'm'
                pos += 1
        elif text[pos] == 's':
            unit = 's'
            pos += 1
        else:
            raise DurationParseError('syntax', pos)
        order = _UNITS[unit][1]
        if order >= last_order:
            raise DurationParseError('order', start)
        last_order = order
        fields.append((_UNITS[unit][0], val, unit, start))
    return fields


def _to_milliseconds(fields):
    total = 0
    for key, val, unit, _ in fields:
        if unit == 'd':
            total += val * 86400000
        elif unit == 'h':
            total += val * 3600000
        elif unit == 'm':
            total += val * 60000
        elif unit == 's':
            total += val * 1000
        elif unit == 'ms':
            total += val
    return total


def _format(total_ms):
    ms = total_ms % 1000
    total_ms //= 1000
    s = total_ms % 60
    total_ms //= 60
    m = total_ms % 60
    total_ms //= 60
    h = total_ms % 24
    d = total_ms // 24
    parts = []
    if d:
        parts.append(f"{d}d")
    if h:
        parts.append(f"{h}h")
    if m:
        parts.append(f"{m}m")
    if s:
        parts.append(f"{s}s")
    if ms:
        parts.append(f"{ms}ms")
    return "".join(parts) if parts else "0s"


def parse_duration(text):
    if not isinstance(text, str):
        raise DurationParseError('type', 0)
    if len(text) == 0:
        raise DurationParseError('empty', 0)
    fields = _tokenize(text)
    for key, val, unit, start in fields:
        max_exclusive = _UNITS[unit][2]
        if max_exclusive is not None and val >= max_exclusive:
            raise DurationParseError('range', start)
    result = {'days': 0, 'hours': 0, 'minutes': 0, 'seconds': 0, 'milliseconds': 0}
    for key, val, unit, _ in fields:
        result[key] = val
    return result


def normalize_duration(text):
    if not isinstance(text, str):
        raise DurationParseError('type', 0)
    if len(text) == 0:
        raise DurationParseError('empty', 0)
    fields = _tokenize(text)
    return _format(_to_milliseconds(fields))
