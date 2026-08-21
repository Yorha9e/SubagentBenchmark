"""Implement the public contract from TASKS.md."""

_UNIT_RANK = {"d": 0, "h": 1, "m": 2, "s": 3, "ms": 4}
_RANGE_LIMITS = {"h": 24, "m": 60, "s": 60, "ms": 1000}
_UNIT_TO_KEY = {
    "d": "days",
    "h": "hours",
    "m": "minutes",
    "s": "seconds",
    "ms": "milliseconds",
}
_KEY_ORDER = ("days", "hours", "minutes", "seconds", "milliseconds")
_UNIT_MILLIS = {"d": 86_400_000, "h": 3_600_000, "m": 60_000, "s": 1_000, "ms": 1}


class DurationParseError(ValueError):
    def __init__(self, code, position):
        self.code = code
        self.position = position
        super().__init__(f"invalid duration: {code} at position {position}")


def _scan(text, check_range):
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if text == "":
        raise DurationParseError("empty", 0)
    fields = []
    last_rank = -1
    pos = 0
    length = len(text)
    while pos < length:
        digits_start = pos
        while pos < length and "0" <= text[pos] <= "9":
            pos += 1
        if pos == digits_start:
            raise DurationParseError("syntax", pos)
        digits = text[digits_start:pos]
        if len(digits) > 1 and digits[0] == "0":
            raise DurationParseError("leading_zero", digits_start)
        unit_start = pos
        if text.startswith("ms", pos):
            unit = "ms"
            pos += 2
        elif pos < length and text[pos] in _UNIT_RANK:
            unit = text[pos]
            pos += 1
        else:
            raise DurationParseError("syntax", unit_start)
        rank = _UNIT_RANK[unit]
        if rank <= last_rank:
            # Strictly increasing rank rejects both wrong order and repeats.
            raise DurationParseError("order", unit_start)
        last_rank = rank
        fields.append((unit, int(digits), digits_start))
    if check_range:
        for unit, value, digits_start in fields:
            limit = _RANGE_LIMITS.get(unit)
            if limit is not None and value >= limit:
                raise DurationParseError("range", digits_start)
    return fields


def parse_duration(text):
    fields = _scan(text, check_range=True)
    values = {key: 0 for key in _KEY_ORDER}
    for unit, value, _digits_start in fields:
        values[_UNIT_TO_KEY[unit]] = value
    return {key: values[key] for key in _KEY_ORDER}


def normalize_duration(text):
    fields = _scan(text, check_range=False)
    total = 0
    for unit, value, _digits_start in fields:
        total += value * _UNIT_MILLIS[unit]
    days, remainder = divmod(total, _UNIT_MILLIS["d"])
    hours, remainder = divmod(remainder, _UNIT_MILLIS["h"])
    minutes, remainder = divmod(remainder, _UNIT_MILLIS["m"])
    seconds, milliseconds = divmod(remainder, _UNIT_MILLIS["s"])
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
    if not parts:
        return "0s"
    return "".join(parts)
