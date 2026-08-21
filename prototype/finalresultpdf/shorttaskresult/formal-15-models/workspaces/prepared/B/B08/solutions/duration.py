"""Implement the public contract from TASKS.md."""


class DurationParseError(ValueError):
    def __init__(self, code, position):
        self.code = code
        self.position = position
        super().__init__(f"{code} at position {position}")


# Unit metadata: unit string -> (rank, output_key, parse_max or None for unbounded)
_UNITS = [
    ("d", 0, "days", None),
    ("h", 1, "hours", 24),
    ("m", 2, "minutes", 60),
    ("s", 3, "seconds", 60),
    ("ms", 4, "milliseconds", 1000),
]

# Map unit string to its info
_UNIT_MAP = {unit: (rank, key, max_val) for unit, rank, key, max_val in _UNITS}

# Output key order
_OUTPUT_KEYS = ["days", "hours", "minutes", "seconds", "milliseconds"]


def _scan_fields(text):
    """
    Scan text and return list of (value, unit, digit_start, unit_start) in order.
    Raises DurationParseError on any syntax error.
    """
    if not isinstance(text, str):
        raise DurationParseError("type", 0)

    if len(text) == 0:
        raise DurationParseError("empty", 0)

    fields = []
    pos = 0
    n = len(text)
    last_rank = -1  # ranks must be strictly increasing (d=0, h=1, m=2, s=3, ms=4)

    while pos < n:
        digit_start = pos

        # Read digits (ASCII only)
        digit_count = 0
        while pos < n and '0' <= text[pos] <= '9':
            digit_count += 1
            pos += 1

        if digit_count == 0:
            raise DurationParseError("syntax", pos)

        # Leading zero check
        if digit_count > 1 and text[digit_start] == '0':
            raise DurationParseError("leading_zero", digit_start)

        value = int(text[digit_start:digit_start + digit_count])

        # Parse unit
        unit_start = pos

        # Try "ms" first (two-char unit)
        if pos + 1 < n and text[pos:pos + 2] == "ms":
            unit = "ms"
            pos += 2
        elif pos < n and text[pos] in ("d", "h", "m", "s"):
            unit = text[pos]
            pos += 1
        else:
            raise DurationParseError("syntax", pos if pos < n else n)

        rank, key, max_val = _UNIT_MAP[unit]

        # Order check: must be strictly increasing rank
        if rank <= last_rank:
            raise DurationParseError("order", unit_start)

        last_rank = rank
        fields.append((value, unit, digit_start, unit_start, key, max_val))

    if not fields:
        raise DurationParseError("syntax", 0)

    return fields


def parse_duration(text):
    fields = _scan_fields(text)

    result = {key: 0 for key in _OUTPUT_KEYS}

    for value, unit, digit_start, unit_start, key, max_val in fields:
        if max_val is not None and value >= max_val:
            raise DurationParseError("range", digit_start)
        result[key] = value

    return result


def normalize_duration(text):
    fields = _scan_fields(text)

    # Convert everything to total milliseconds
    total_ms = 0
    for value, unit, digit_start, unit_start, key, max_val in fields:
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

    # Break down into canonical form
    remaining = total_ms
    parts = []

    days, remaining = divmod(remaining, 24 * 60 * 60 * 1000)
    if days > 0:
        parts.append(f"{days}d")

    hours, remaining = divmod(remaining, 60 * 60 * 1000)
    if hours > 0:
        parts.append(f"{hours}h")

    minutes, remaining = divmod(remaining, 60 * 1000)
    if minutes > 0:
        parts.append(f"{minutes}m")

    seconds, remaining = divmod(remaining, 1000)
    if seconds > 0:
        parts.append(f"{seconds}s")

    milliseconds = remaining
    if milliseconds > 0:
        parts.append(f"{milliseconds}ms")

    return "".join(parts)
