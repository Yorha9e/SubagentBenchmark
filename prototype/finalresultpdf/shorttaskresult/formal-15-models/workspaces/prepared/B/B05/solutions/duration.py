class DurationParseError(ValueError):
    def __init__(self, code, position):
        self.code = code
        self.position = position
        super().__init__(f"Duration parse error: {code} at position {position}")


_UNITS = ["d", "h", "m", "s", "ms"]
_KEYS = ["days", "hours", "minutes", "seconds", "milliseconds"]
_RANGES = [None, 24, 60, 60, 1000]


def _next_unit_index(unit):
    if unit == "ms":
        return 4
    if unit in _UNITS[:4]:
        return _UNITS.index(unit)
    return -1


def _parse_fields(text):
    fields = []
    i = 0
    last_unit_rank = -1

    while i < len(text):
        num_start = i
        if not ('0' <= text[i] <= '9'):
            raise DurationParseError("syntax", i)

        if text[i] == '0' and i + 1 < len(text) and '0' <= text[i + 1] <= '9':
            raise DurationParseError("leading_zero", num_start)

        num = 0
        while i < len(text) and '0' <= text[i] <= '9':
            num = num * 10 + (ord(text[i]) - ord('0'))
            i += 1

        unit_start = i
        if i >= len(text):
            raise DurationParseError("syntax", i)

        if text[i:i + 2] == "ms":
            unit = "ms"
            i += 2
        elif text[i] in _UNITS[:4]:
            unit = text[i]
            i += 1
        else:
            raise DurationParseError("syntax", unit_start)

        unit_idx = _next_unit_index(unit)
        if unit_idx <= last_unit_rank:
            raise DurationParseError("order", unit_start)
        last_unit_rank = unit_idx

        fields.append((num, unit_idx, num_start, unit_start))

    return fields


def parse_duration(text):
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if text == "":
        raise DurationParseError("empty", 0)

    fields = _parse_fields(text)

    result = {k: 0 for k in _KEYS}
    for num, unit_idx, num_start, unit_start in fields:
        key = _KEYS[unit_idx]
        if unit_idx > 0 and num >= _RANGES[unit_idx]:
            raise DurationParseError("range", num_start)
        result[key] = num

    return result


def normalize_duration(text):
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if text == "":
        raise DurationParseError("empty", 0)

    fields = _parse_fields(text)

    total_ms = 0
    for num, unit_idx, num_start, unit_start in fields:
        if unit_idx == 0:
            total_ms += num * 24 * 60 * 60 * 1000
        elif unit_idx == 1:
            total_ms += num * 60 * 60 * 1000
        elif unit_idx == 2:
            total_ms += num * 60 * 1000
        elif unit_idx == 3:
            total_ms += num * 1000
        elif unit_idx == 4:
            total_ms += num

    days, rem = divmod(total_ms, 24 * 60 * 60 * 1000)
    hours, rem = divmod(rem, 60 * 60 * 1000)
    minutes, rem = divmod(rem, 60 * 1000)
    seconds, ms = divmod(rem, 1000)

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

    if not parts:
        return "0s"

    return "".join(parts)
