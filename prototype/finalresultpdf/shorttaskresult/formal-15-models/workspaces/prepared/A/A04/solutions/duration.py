"""Implement the public contract from TASKS.md."""


class DurationParseError(ValueError):
    def __init__(self, code, position, message=None):
        self.code = code
        self.position = position
        if message is None:
            message = f"duration parse error: {code} at position {position}"
        super().__init__(message)


_UNIT_RANK = {
    "d": 0,
    "h": 1,
    "m": 2,
    "s": 3,
    "ms": 4,
}

_UNIT_LENGTH = {
    "d": 1,
    "h": 1,
    "m": 1,
    "s": 1,
    "ms": 2,
}

_RANGE_LIMITS = {
    "h": 24,
    "m": 60,
    "s": 60,
    "ms": 1000,
}

_MILLIS_PER_UNIT = {
    "d": 24 * 60 * 60 * 1000,
    "h": 60 * 60 * 1000,
    "m": 60 * 1000,
    "s": 1000,
    "ms": 1,
}


def _parse(text, check_ranges):
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if text == "":
        raise DurationParseError("empty", 0)

    fields = {}
    starts = {}
    prev_rank = -1
    i = 0
    n = len(text)

    while i < n:
        if not text[i].isdigit():
            raise DurationParseError("syntax", i)

        start = i
        while i < n and text[i].isdigit():
            i += 1

        digits = text[start:i]
        if digits[0] == "0" and len(digits) > 1:
            raise DurationParseError("leading_zero", start)

        if i + 1 < n and text[i] == "m" and text[i + 1] == "s":
            unit = "ms"
        elif i < n and text[i] in _UNIT_RANK:
            unit = text[i]
        else:
            raise DurationParseError("syntax", i if i < n else n)

        i += _UNIT_LENGTH[unit]
        rank = _UNIT_RANK[unit]

        if rank <= prev_rank:
            raise DurationParseError("order", start)
        prev_rank = rank

        fields[unit] = int(digits)
        starts[unit] = start

    if not fields:
        raise DurationParseError("empty", 0)

    if check_ranges:
        for unit, limit in _RANGE_LIMITS.items():
            if unit in fields and fields[unit] >= limit:
                raise DurationParseError("range", starts[unit])

    return fields


def parse_duration(text):
    fields = _parse(text, check_ranges=True)
    return {
        "days": fields.get("d", 0),
        "hours": fields.get("h", 0),
        "minutes": fields.get("m", 0),
        "seconds": fields.get("s", 0),
        "milliseconds": fields.get("ms", 0),
    }


def normalize_duration(text):
    fields = _parse(text, check_ranges=False)

    total_ms = sum(fields[unit] * _MILLIS_PER_UNIT[unit] for unit in fields)

    days, rem = divmod(total_ms, _MILLIS_PER_UNIT["d"])
    hours, rem = divmod(rem, _MILLIS_PER_UNIT["h"])
    minutes, rem = divmod(rem, _MILLIS_PER_UNIT["m"])
    seconds, milliseconds = divmod(rem, _MILLIS_PER_UNIT["s"])

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
