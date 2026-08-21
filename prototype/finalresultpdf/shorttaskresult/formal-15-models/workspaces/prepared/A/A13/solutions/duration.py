"""Implement the public contract from TASKS.md."""

_UNITS = ["d", "h", "m", "s", "ms"]
_UNIT_KEY = {"d": "days", "h": "hours", "m": "minutes", "s": "seconds", "ms": "milliseconds"}
_RANGES = {"h": 24, "m": 60, "s": 60, "ms": 1000}


class DurationParseError(ValueError):
    def __init__(self, code, position):
        self.code = code
        self.position = position
        super().__init__(f"DurationParseError({code}, {position})")


def _validate_type(text):
    if not isinstance(text, str):
        raise DurationParseError("type", 0)


def _parse_fields(text):
    _validate_type(text)
    if not text:
        raise DurationParseError("empty", 0)

    fields = []
    i = 0

    while i < len(text):
        if not text[i].isdigit():
            raise DurationParseError("syntax", i)

        num_start = i
        while i < len(text) and text[i].isdigit():
            i += 1

        num_str = text[num_start:i]
        if len(num_str) > 1 and num_str[0] == "0":
            raise DurationParseError("leading_zero", num_start)

        matched = None
        for unit in _UNITS:
            if text[i : i + len(unit)] == unit:
                matched = unit
                break

        if matched is None:
            raise DurationParseError("syntax", i)

        if fields:
            prev_idx = _UNITS.index(fields[-1][0])
            cur_idx = _UNITS.index(matched)
            if cur_idx <= prev_idx:
                raise DurationParseError("order", num_start)

        fields.append((matched, int(num_str), num_start))
        i += len(matched)

    if not fields:
        raise DurationParseError("empty", 0)

    return fields


def parse_duration(text):
    fields = _parse_fields(text)
    result = {"days": 0, "hours": 0, "minutes": 0, "seconds": 0, "milliseconds": 0}
    for unit, value, pos in fields:
        result[_UNIT_KEY[unit]] = value
        if unit in _RANGES:
            if value < 0 or value >= _RANGES[unit]:
                raise DurationParseError("range", pos)
    return result


def normalize_duration(text):
    fields = _parse_fields(text)

    total_ms = 0
    for unit, value, _pos in fields:
        if unit == "d":
            total_ms += value * 86400000
        elif unit == "h":
            total_ms += value * 3600000
        elif unit == "m":
            total_ms += value * 60000
        elif unit == "s":
            total_ms += value * 1000
        else:
            total_ms += value

    if total_ms == 0:
        return "0s"

    parts = []
    d, total_ms = divmod(total_ms, 86400000)
    h, total_ms = divmod(total_ms, 3600000)
    m, total_ms = divmod(total_ms, 60000)
    s, ms = divmod(total_ms, 1000)

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

    return "".join(parts)
