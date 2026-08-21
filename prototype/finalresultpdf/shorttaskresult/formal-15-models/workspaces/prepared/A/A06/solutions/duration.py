"""Implement the public contract from TASKS.md."""

_UNIT_ORDER = {"d": 0, "h": 1, "m": 2, "s": 3, "ms": 4}
_UNIT_MILLIS = {"d": 86_400_000, "h": 3_600_000, "m": 60_000, "s": 1_000, "ms": 1}
_PARSE_LIMITS = {"h": 24, "m": 60, "s": 60, "ms": 1000}
_DIGITS = frozenset("0123456789")


class DurationParseError(ValueError):
    def __init__(self, code, position=0, message=None):
        self.code = code
        self.position = position
        if message is None:
            message = f"duration {code} error at position {position}"
        super().__init__(message)


def _fail(code, position):
    raise DurationParseError(code, position)


def _fields(text):
    fields = []
    index = 0
    end = len(text)
    last_order = -1
    while index < end:
        start = index
        if text[index] not in _DIGITS:
            _fail("syntax", index)
        while index < end and text[index] in _DIGITS:
            index += 1
        unit_start = index
        if index < end and text[index] == "m" and index + 1 < end and text[index + 1] == "s":
            unit = "ms"
            index += 2
        elif index < end and text[index] in "dhms":
            unit = text[index]
            index += 1
        else:
            _fail("syntax", unit_start)
        number = text[start:unit_start]
        if len(number) > 1 and number[0] == "0":
            _fail("leading_zero", start)
        order = _UNIT_ORDER[unit]
        if order <= last_order:
            _fail("order", unit_start)
        last_order = order
        fields.append((unit, int(number), start))
    return fields


def parse_duration(text):
    if not isinstance(text, str):
        _fail("type", 0)
    if text == "":
        _fail("empty", 0)
    fields = _fields(text)
    values = {"d": 0, "h": 0, "m": 0, "s": 0, "ms": 0}
    for unit, amount, start in fields:
        limit = _PARSE_LIMITS.get(unit)
        if limit is not None and amount >= limit:
            _fail("range", start)
        values[unit] = amount
    return {
        "days": values["d"],
        "hours": values["h"],
        "minutes": values["m"],
        "seconds": values["s"],
        "milliseconds": values["ms"],
    }


def normalize_duration(text):
    if not isinstance(text, str):
        _fail("type", 0)
    if text == "":
        _fail("empty", 0)
    fields = _fields(text)
    total = sum(_UNIT_MILLIS[unit] * amount for unit, amount, _ in fields)
    if total == 0:
        return "0s"
    parts = []
    for unit in ("d", "h", "m", "s"):
        amount, total = divmod(total, _UNIT_MILLIS[unit])
        if amount:
            parts.append(f"{amount}{unit}")
    if total:
        parts.append(f"{total}ms")
    return "".join(parts)
