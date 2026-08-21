"""Implement the public contract from TASKS.md."""


class DurationParseError(ValueError):
    def __init__(self, code, position):
        self.code = code
        self.position = position
        super().__init__("{} at position {}".format(code, position))


_UNITS = {"d": 0, "h": 1, "m": 2, "s": 3, "ms": 4}
_FACTORS = {
    "d": 24 * 60 * 60 * 1000,
    "h": 60 * 60 * 1000,
    "m": 60 * 1000,
    "s": 1000,
    "ms": 1,
}
_LIMITS = {"h": 24, "m": 60, "s": 60, "ms": 1000}


def _decimal_value(digits):
    value = 0
    for character in digits:
        value = value * 10 + ord(character) - ord("0")
    return value


def _parse_fields(text):
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if not text:
        raise DurationParseError("empty", 0)

    fields = []
    position = 0
    previous_unit = -1
    length = len(text)

    while position < length:
        start = position
        if not ("0" <= text[position] <= "9"):
            raise DurationParseError("syntax", position)

        while position < length and "0" <= text[position] <= "9":
            position += 1
        digits_end = position

        if digits_end - start > 1 and text[start] == "0":
            raise DurationParseError("leading_zero", start)

        if text.startswith("ms", position):
            unit = "ms"
            position += 2
        elif position < length and text[position] in "dhms":
            unit = text[position]
            position += 1
        else:
            raise DurationParseError("syntax", position)

        unit_order = _UNITS[unit]
        if unit_order <= previous_unit:
            raise DurationParseError("order", start)
        previous_unit = unit_order
        fields.append((_decimal_value(text[start:digits_end]), unit, start))

    return fields


def parse_duration(text):
    fields = _parse_fields(text)
    values = {
        "days": 0,
        "hours": 0,
        "minutes": 0,
        "seconds": 0,
        "milliseconds": 0,
    }
    names = {
        "d": "days",
        "h": "hours",
        "m": "minutes",
        "s": "seconds",
        "ms": "milliseconds",
    }

    for value, unit, start in fields:
        limit = _LIMITS.get(unit)
        if limit is not None and value >= limit:
            raise DurationParseError("range", start)
        values[names[unit]] = value

    return values


def _decimal_text(value):
    if value == 0:
        return "0"

    chunks = []
    base = 1_000_000_000
    while value:
        value, remainder = divmod(value, base)
        chunks.append(remainder)

    result = str(chunks.pop())
    while chunks:
        result += "{:09d}".format(chunks.pop())
    return result


def normalize_duration(text):
    fields = _parse_fields(text)
    total = 0
    for value, unit, _ in fields:
        total += value * _FACTORS[unit]

    output = []
    for unit, suffix, factor in (
        ("d", "d", _FACTORS["d"]),
        ("h", "h", _FACTORS["h"]),
        ("m", "m", _FACTORS["m"]),
        ("s", "s", _FACTORS["s"]),
        ("ms", "ms", _FACTORS["ms"]),
    ):
        value, total = divmod(total, factor)
        if value:
            output.append(_decimal_text(value) + suffix)

    return "".join(output) or "0s"
