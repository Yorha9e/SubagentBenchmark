"""Implement the public contract from TASKS.md."""


class DurationParseError(ValueError):
    def __init__(self, message, code, position):
        super().__init__(message)
        self.code = code
        self.position = position


# Units appear in strict descending order in the string.
_UNIT_PRIORITY = {"d": 0, "h": 1, "m": 2, "s": 3, "ms": 4}
# Try longer units first so "ms" wins over "m" when both could match.
_UNIT_MATCH_ORDER = ["ms", "s", "m", "h", "d"]


def _parse_fields(text):
    if not isinstance(text, str):
        raise DurationParseError("text must be a string", "type", 0)
    if not text:
        raise DurationParseError("text is empty", "empty", 0)

    fields = []  # list of (value_int, unit, value_start)
    i = 0
    n = len(text)
    while i < n:
        if not text[i].isdigit():
            raise DurationParseError(
                "expected digit at position {}".format(i), "syntax", i
            )

        value_start = i
        while i < n and text[i].isdigit():
            i += 1
        value_str = text[value_start:i]

        if len(value_str) > 1 and value_str[0] == "0":
            raise DurationParseError(
                "leading zero at position {}".format(value_start),
                "leading_zero",
                value_start,
            )

        if i >= n:
            raise DurationParseError(
                "missing unit at position {}".format(i), "syntax", i
            )

        matched_unit = None
        for u in _UNIT_MATCH_ORDER:
            if text[i:].startswith(u):
                matched_unit = u
                break
        if matched_unit is None:
            raise DurationParseError(
                "unknown unit at position {}".format(i), "syntax", i
            )

        fields.append((int(value_str), matched_unit, value_start))
        i += len(matched_unit)

    if not fields:
        raise DurationParseError("text is empty", "empty", 0)

    # Check strict descending unit order; repeats are reported as order errors.
    last_priority = -1
    for value, unit, value_start in fields:
        p = _UNIT_PRIORITY[unit]
        if p <= last_priority:
            raise DurationParseError(
                "unit order violation at position {}".format(value_start),
                "order",
                value_start,
            )
        last_priority = p

    return fields


def parse_duration(text):
    fields = _parse_fields(text)

    for value, unit, value_start in fields:
        if unit == "h" and value >= 24:
            raise DurationParseError(
                "hours out of range at position {}".format(value_start),
                "range",
                value_start,
            )
        if unit == "m" and value >= 60:
            raise DurationParseError(
                "minutes out of range at position {}".format(value_start),
                "range",
                value_start,
            )
        if unit == "s" and value >= 60:
            raise DurationParseError(
                "seconds out of range at position {}".format(value_start),
                "range",
                value_start,
            )
        if unit == "ms" and value >= 1000:
            raise DurationParseError(
                "milliseconds out of range at position {}".format(value_start),
                "range",
                value_start,
            )

    result = {
        "days": 0,
        "hours": 0,
        "minutes": 0,
        "seconds": 0,
        "milliseconds": 0,
    }
    for value, unit, _ in fields:
        if unit == "d":
            result["days"] = value
        elif unit == "h":
            result["hours"] = value
        elif unit == "m":
            result["minutes"] = value
        elif unit == "s":
            result["seconds"] = value
        elif unit == "ms":
            result["milliseconds"] = value
    return result


def normalize_duration(text):
    fields = _parse_fields(text)

    total_ms = 0
    for value, unit, _ in fields:
        if unit == "d":
            total_ms += value * 86400000
        elif unit == "h":
            total_ms += value * 3600000
        elif unit == "m":
            total_ms += value * 60000
        elif unit == "s":
            total_ms += value * 1000
        elif unit == "ms":
            total_ms += value

    d, rem = divmod(total_ms, 86400000)
    h, rem = divmod(rem, 3600000)
    m, rem = divmod(rem, 60000)
    s, ms = divmod(rem, 1000)

    parts = []
    if d > 0:
        parts.append("{}d".format(d))
    if h > 0:
        parts.append("{}h".format(h))
    if m > 0:
        parts.append("{}m".format(m))
    if s > 0:
        parts.append("{}s".format(s))
    if ms > 0:
        parts.append("{}ms".format(ms))

    if not parts:
        return "0s"
    return "".join(parts)
