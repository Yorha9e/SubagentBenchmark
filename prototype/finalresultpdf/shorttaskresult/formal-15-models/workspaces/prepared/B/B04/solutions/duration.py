"""Implement the public contract from TASKS.md."""


class DurationParseError(ValueError):
    def __init__(self, code, position, message=None):
        self.code = code
        self.position = position
        if message is None:
            message = f"{code} at position {position}"
        super().__init__(message)


_UNITS = ("d", "h", "m", "s", "ms")
_OUTPUT_KEYS = ("days", "hours", "minutes", "seconds", "milliseconds")
_UNIT_TO_RANK = {"d": 0, "h": 1, "m": 2, "s": 3, "ms": 4}
_RANGES = {"h": 24, "m": 60, "s": 60, "ms": 1000}


def _scan_fields(text):
    """Return list of (unit, value, digit_pos, unit_pos) or raise early errors."""
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if text == "":
        raise DurationParseError("empty", 0)

    fields = []
    pos = 0
    last_rank = -1
    n = len(text)

    while pos < n:
        digit_pos = pos
        if not ("0" <= text[pos] <= "9"):
            raise DurationParseError("syntax", pos)

        while pos < n and "0" <= text[pos] <= "9":
            pos += 1

        digits = text[digit_pos:pos]
        if len(digits) > 1 and digits[0] == "0":
            raise DurationParseError("leading_zero", digit_pos)

        if pos >= n:
            raise DurationParseError("syntax", pos)

        unit_pos = pos
        if text.startswith("ms", pos):
            unit = "ms"
            pos += 2
        elif pos < n and text[pos] in _UNIT_TO_RANK:
            unit = text[pos]
            pos += 1
        else:
            raise DurationParseError("syntax", pos)

        rank = _UNIT_TO_RANK[unit]
        if rank <= last_rank:
            raise DurationParseError("order", unit_pos)
        last_rank = rank

        value = int(digits)
        fields.append((unit, value, digit_pos, unit_pos))

    if not fields:
        raise DurationParseError("syntax", 0)

    return fields


def parse_duration(text):
    fields = _scan_fields(text)

    for unit, value, digit_pos, _ in fields:
        if unit in _RANGES and value >= _RANGES[unit]:
            raise DurationParseError("range", digit_pos)

    result = {}
    for key in _OUTPUT_KEYS:
        result[key] = 0
    for unit, value, _, _ in fields:
        result[_OUTPUT_KEYS[_UNIT_TO_RANK[unit]]] = value
    return result


def normalize_duration(text):
    fields = _scan_fields(text)

    total_ms = 0
    for unit, value, _, _ in fields:
        if unit == "d":
            total_ms += value * 24 * 60 * 60 * 1000
        elif unit == "h":
            total_ms += value * 60 * 60 * 1000
        elif unit == "m":
            total_ms += value * 60 * 1000
        elif unit == "s":
            total_ms += value * 1000
        elif unit == "ms":
            total_ms += value

    if total_ms == 0:
        return "0s"

    ms = total_ms % 1000
    total_seconds = total_ms // 1000
    seconds = total_seconds % 60
    total_minutes = total_seconds // 60
    minutes = total_minutes % 60
    total_hours = total_minutes // 60
    hours = total_hours % 24
    days = total_hours // 24

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds:
        parts.append(f"{seconds}s")
    if ms:
        parts.append(f"{ms}ms")

    return "".join(parts)
