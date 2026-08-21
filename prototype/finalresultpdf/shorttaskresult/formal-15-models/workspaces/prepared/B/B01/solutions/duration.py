"""Implement the public contract from TASKS.md."""


UNITS = ["d", "h", "m", "s", "ms"]
UNIT_RANK = {"d": 0, "h": 1, "m": 2, "s": 3, "ms": 4}
UNIT_TO_KEY = {
    "d": "days",
    "h": "hours",
    "m": "minutes",
    "s": "seconds",
    "ms": "milliseconds",
}
OUTPUT_KEYS = ["days", "hours", "minutes", "seconds", "milliseconds"]
PARSE_CAP = {"h": 24, "m": 60, "s": 60, "ms": 1000}
MS_PER_UNIT = {"ms": 1, "s": 1000, "m": 60000, "h": 3600000, "d": 86400000}


class DurationParseError(ValueError):
    def __init__(self, code, position):
        self.code = code
        self.position = position
        super().__init__(f"{code} at {position}")


def _scan(text):
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if len(text) == 0:
        raise DurationParseError("empty", 0)
    fields = []
    last_rank = -1
    i = 0
    n = len(text)
    while i < n:
        if not ("0" <= text[i] <= "9"):
            raise DurationParseError("syntax", i)
        digit_start = i
        while i < n and "0" <= text[i] <= "9":
            i += 1
        num_str = text[digit_start:i]
        if len(num_str) > 1 and num_str[0] == "0":
            raise DurationParseError("leading_zero", digit_start)
        value = int(num_str)
        unit_start = i
        if i < n and text[i : i + 2] == "ms":
            unit = "ms"
            i += 2
        elif i < n and text[i] in "dhms":
            unit = text[i]
            i += 1
        else:
            raise DurationParseError("syntax", i if i < n else n)
        rank = UNIT_RANK[unit]
        if rank <= last_rank:
            raise DurationParseError("order", unit_start)
        last_rank = rank
        fields.append((unit, value, digit_start, unit_start))
    return fields


def parse_duration(text):
    fields = _scan(text)
    result = {
        "days": 0,
        "hours": 0,
        "minutes": 0,
        "seconds": 0,
        "milliseconds": 0,
    }
    for unit, value, digit_start, unit_start in fields:
        cap = PARSE_CAP.get(unit)
        if cap is not None and value >= cap:
            raise DurationParseError("range", digit_start)
        result[UNIT_TO_KEY[unit]] = value
    return result


def normalize_duration(text):
    fields = _scan(text)
    total_ms = 0
    for unit, value, digit_start, unit_start in fields:
        total_ms += value * MS_PER_UNIT[unit]
    d, rem = divmod(total_ms, 86400000)
    h, rem = divmod(rem, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)
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
    if not parts:
        return "0s"
    return "".join(parts)
