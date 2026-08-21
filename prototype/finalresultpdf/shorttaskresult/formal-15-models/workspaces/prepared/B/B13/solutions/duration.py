"""Implement the public contract from TASKS.md."""


class DurationParseError(ValueError):
    """Error raised for invalid duration strings."""

    def __init__(self, code, position):
        self.code = code
        self.position = position
        super().__init__(f"duration parse error: code={code!r} at position {position}")


# Unit order: d > h > m > s > ms
_UNITS = ["d", "h", "m", "s", "ms"]
_UNIT_RANK = {"d": 0, "h": 1, "m": 2, "s": 3, "ms": 4}

# Output keys in fixed order
_OUTPUT_KEYS = ["days", "hours", "minutes", "seconds", "milliseconds"]

# Parse limits (subordinate ranges)
_PARSE_LIMITS = {"h": 24, "m": 60, "s": 60, "ms": 1000}


def _parse_fields(text):
    """Parse duration string into list of (unit_rank, numeric_value, num_start, unit_start).

    Raises DurationParseError on invalid input.
    """
    if not isinstance(text, str):
        raise DurationParseError("type", 0)

    if len(text) == 0:
        raise DurationParseError("empty", 0)

    fields = []
    pos = 0
    last_rank = -1

    while pos < len(text):
        num_start = pos

        # Read digits
        if pos >= len(text) or not ('0' <= text[pos] <= '9'):
            raise DurationParseError("syntax", pos)

        while pos < len(text) and '0' <= text[pos] <= '9':
            pos += 1

        num_str = text[num_start:pos]

        # Leading zero check
        if len(num_str) > 1 and num_str[0] == '0':
            raise DurationParseError("leading_zero", num_start)

        value = int(num_str)

        # Read unit
        unit_start = pos
        if pos + 1 < len(text) and text[pos:pos+2] == "ms":
            unit = "ms"
            pos += 2
        elif pos < len(text) and text[pos] in ("d", "h", "m", "s"):
            unit = text[pos]
            pos += 1
        else:
            # No valid unit found
            raise DurationParseError("syntax", pos)

        rank = _UNIT_RANK[unit]

        # Order check: must be strictly increasing rank
        if rank <= last_rank:
            raise DurationParseError("order", unit_start)

        last_rank = rank
        fields.append((rank, value, num_start, unit_start))

    return fields


def parse_duration(text):
    """Parse a duration string into a dict with all five keys."""
    fields = _parse_fields(text)

    # Range check for parse
    for rank, value, num_start, unit_start in fields:
        unit = _UNITS[rank]
        if unit in _PARSE_LIMITS:
            if value >= _PARSE_LIMITS[unit]:
                raise DurationParseError("range", num_start)

    # Build result dict
    result = {"days": 0, "hours": 0, "minutes": 0, "seconds": 0, "milliseconds": 0}
    unit_to_key = {"d": "days", "h": "hours", "m": "minutes", "s": "seconds", "ms": "milliseconds"}

    for rank, value, num_start, unit_start in fields:
        unit = _UNITS[rank]
        result[unit_to_key[unit]] = value

    return result


def normalize_duration(text):
    """Normalize a duration string to shortest canonical form."""
    fields = _parse_fields(text)

    # Convert all to milliseconds (as integer)
    total_ms = 0
    multipliers = {"d": 86400000, "h": 3600000, "m": 60000, "s": 1000, "ms": 1}

    for rank, value, num_start, unit_start in fields:
        unit = _UNITS[rank]
        total_ms += value * multipliers[unit]

    if total_ms == 0:
        return "0s"

    # Decompose back into units
    parts = []
    remaining = total_ms

    for unit, mult in [("d", 86400000), ("h", 3600000), ("m", 60000), ("s", 1000), ("ms", 1)]:
        if mult > 1:
            q, remaining = divmod(remaining, mult)
        else:
            q = remaining
            remaining = 0
        if q > 0:
            parts.append(f"{q}{unit}")

    return "".join(parts)
