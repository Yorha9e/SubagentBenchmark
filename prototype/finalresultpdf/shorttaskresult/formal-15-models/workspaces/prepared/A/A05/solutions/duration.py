"""Implement the public contract from TASKS.md."""


class DurationParseError(ValueError):
    def __init__(self, code, position):
        self.code = code
        self.position = position
        super().__init__(f"{code}:{position}")


UNIT_ORDER = ["d", "h", "m", "s", "ms"]
UNIT_NAME = {"d": "days", "h": "hours", "m": "minutes", "s": "seconds", "ms": "milliseconds"}
RANGE_LIMIT = {"h": 24, "m": 60, "s": 60, "ms": 1000}
OUTPUT_KEYS = ["days", "hours", "minutes", "seconds", "milliseconds"]


def _check_type(text):
    if type(text) is not str:
        raise DurationParseError("type", 0)


def _parse_fields(text, check_range=True):
    _check_type(text)
    if text == "":
        raise DurationParseError("empty", 0)

    values = {}
    fields = []
    last_unit_idx = -1
    i = 0
    n = len(text)

    while i < n:
        # Leading zero check (except single "0")
        if text[i] == "0" and i + 1 < n and text[i + 1].isdigit():
            raise DurationParseError("leading_zero", i)

        # Parse number
        j = i
        while j < n and text[j].isdigit():
            j += 1
        num_str = text[i:j]
        if not num_str:
            raise DurationParseError("syntax", i)

        # Parse unit
        unit = None
        if j < n and text[j : j + 2] == "ms":
            unit = "ms"
            j += 2
        elif j < n and text[j] in "dhms":
            unit = text[j]
            j += 1
        else:
            raise DurationParseError("syntax", i)

        # Order and uniqueness
        unit_idx = UNIT_ORDER.index(unit)
        if unit_idx <= last_unit_idx or unit in values:
            raise DurationParseError("order", i)

        val = int(num_str)
        values[unit] = val
        fields.append((unit, val, i))
        i = j
        last_unit_idx = unit_idx

    if check_range:
        for unit, limit in RANGE_LIMIT.items():
            for u, v, pos in fields:
                if u == unit and v >= limit:
                    raise DurationParseError("range", pos)

    return values


def parse_duration(text):
    values = _parse_fields(text, check_range=True)
    result = {k: 0 for k in OUTPUT_KEYS}
    for unit, val in values.items():
        result[UNIT_NAME[unit]] = val
    return result


def normalize_duration(text):
    values = _parse_fields(text, check_range=False)

    total_ms = values.get("ms", 0)
    total_s = values.get("s", 0)
    total_m = values.get("m", 0)
    total_h = values.get("h", 0)
    total_d = values.get("d", 0)

    carry, total_ms = divmod(total_ms, 1000)
    total_s += carry
    carry, total_s = divmod(total_s, 60)
    total_m += carry
    carry, total_m = divmod(total_m, 60)
    total_h += carry
    carry, total_h = divmod(total_h, 24)
    total_d += carry

    parts = []
    if total_d:
        parts.append(f"{total_d}d")
    if total_h:
        parts.append(f"{total_h}h")
    if total_m:
        parts.append(f"{total_m}m")
    if total_s:
        parts.append(f"{total_s}s")
    if total_ms:
        parts.append(f"{total_ms}ms")

    if not parts:
        return "0s"

    return "".join(parts)
