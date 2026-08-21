_UNIT_ORDER = {"d": 0, "h": 1, "m": 2, "s": 3, "ms": 4}
_UNIT_KEY = {
    "d": "days", "h": "hours", "m": "minutes",
    "s": "seconds", "ms": "milliseconds",
}
_UNIT_MS = {"d": 86_400_000, "h": 3_600_000, "m": 60_000, "s": 1_000, "ms": 1}
_RANGES = {"d": None, "h": 24, "m": 60, "s": 60, "ms": 1000}
_DIGITS = "0123456789"


class DurationParseError(ValueError):
    """Raised for invalid duration input."""

    def __init__(self, code="", position=0, message=""):
        self.code = code
        self.position = position
        super().__init__(
            message or f"duration parse error: {code} at position {position}"
        )


def _parse_fields(text):
    """Parse *text* into a list of ``(value_str, unit, start_pos)`` tuples.

    Raises :class:`DurationParseError` for type / empty / syntax /
    leading_zero problems.
    """
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if not text:
        raise DurationParseError("empty", 0)

    fields = []
    pos = 0
    n = len(text)

    while pos < n:
        start = pos
        # --- digits ---------------------------------------------------
        if text[pos] not in _DIGITS:
            raise DurationParseError("syntax", pos)
        while pos < n and text[pos] in _DIGITS:
            pos += 1
        value_str = text[start:pos]
        # Leading zeroes are forbidden except the single value "0".
        if len(value_str) > 1 and value_str[0] == "0":
            raise DurationParseError("leading_zero", start)
        # --- unit -----------------------------------------------------
        if pos >= n:
            raise DurationParseError("syntax", pos)
        if text[pos:pos + 2] == "ms":
            unit = "ms"
            pos += 2
        elif text[pos] in "dhms":
            unit = text[pos]
            pos += 1
        else:
            raise DurationParseError("syntax", pos)
        fields.append((value_str, unit, start))

    return fields


def _validate_order(fields):
    """Ensure units are in strict descending order without repetition."""
    prev_order = -1
    for _, unit, start in fields:
        current = _UNIT_ORDER[unit]
        if current <= prev_order:
            raise DurationParseError("order", start)
        prev_order = current


def parse_duration(text):
    """Parse a duration string into a plain dict.

    Returns ``{days, hours, minutes, seconds, milliseconds}`` with every
    key present (zero-filled) in that fixed order.
    """
    fields = _parse_fields(text)
    _validate_order(fields)
    result = {
        "days": 0, "hours": 0, "minutes": 0,
        "seconds": 0, "milliseconds": 0,
    }
    for value_str, unit, start in fields:
        value = int(value_str)
        limit = _RANGES[unit]
        if limit is not None and value >= limit:
            raise DurationParseError("range", start)
        result[_UNIT_KEY[unit]] = value
    return result


def normalize_duration(text):
    """Normalise a duration string to its shortest canonical form.

    Accepts syntactically valid out-of-range subordinate fields and carries
    overflow into larger units.  Zero fields are omitted except the canonical
    zero which is ``"0s"``.  The result is idempotent.
    """
    fields = _parse_fields(text)
    _validate_order(fields)

    total_ms = 0
    for value_str, unit, _ in fields:
        total_ms += int(value_str) * _UNIT_MS[unit]

    days, total_ms = divmod(total_ms, 86_400_000)
    hours, total_ms = divmod(total_ms, 3_600_000)
    minutes, total_ms = divmod(total_ms, 60_000)
    seconds, milliseconds = divmod(total_ms, 1_000)

    parts = []
    if days:
        parts.append(f"{days}d")
    if hours:
        parts.append(f"{hours}h")
    if minutes:
        parts.append(f"{minutes}m")
    if seconds:
        parts.append(f"{seconds}s")
    if milliseconds:
        parts.append(f"{milliseconds}ms")
    return "".join(parts) if parts else "0s"
