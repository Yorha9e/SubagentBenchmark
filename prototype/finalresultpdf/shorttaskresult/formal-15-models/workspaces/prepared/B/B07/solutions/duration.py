"""Parse and normalize compact duration strings."""


_UNIT_RANK = {"d": 0, "h": 1, "m": 2, "s": 3, "ms": 4}
_UNIT_MILLISECONDS = {
    "d": 86_400_000,
    "h": 3_600_000,
    "m": 60_000,
    "s": 1_000,
    "ms": 1,
}
_RANGE_LIMITS = {"h": 24, "m": 60, "s": 60, "ms": 1_000}


class DurationParseError(ValueError):
    def __init__(self, code, position, message=None):
        self.code = code
        self.position = position
        if message is None:
            message = f"invalid duration ({code}) at position {position}"
        super().__init__(message)


def _error(code, position):
    return DurationParseError(code, position)


def _decimal_value(digits):
    value = 0
    for character in digits:
        value = value * 10 + (ord(character) - ord("0"))
    return value


def _scan(text):
    if not isinstance(text, str):
        raise _error("type", 0)
    if text == "":
        raise _error("empty", 0)

    fields = []
    position = 0
    previous_rank = -1
    length = len(text)

    while position < length:
        if not ("0" <= text[position] <= "9"):
            raise _error("syntax", position)

        number_start = position
        while position < length and "0" <= text[position] <= "9":
            position += 1
        digits = text[number_start:position]
        if len(digits) > 1 and digits[0] == "0":
            raise _error("leading_zero", number_start)
        value = _decimal_value(digits)

        unit_start = position
        if text.startswith("ms", position):
            unit = "ms"
            position += 2
        elif position < length and text[position] in "dhms":
            unit = text[position]
            position += 1
        else:
            raise _error("syntax", unit_start)

        rank = _UNIT_RANK[unit]
        if rank <= previous_rank:
            raise _error("order", unit_start)
        previous_rank = rank
        fields.append((unit, value, number_start, unit_start))

    return fields


def parse_duration(text):
    fields = _scan(text)
    values = {"d": 0, "h": 0, "m": 0, "s": 0, "ms": 0}
    for unit, value, number_start, _unit_start in fields:
        limit = _RANGE_LIMITS.get(unit)
        if limit is not None and value >= limit:
            raise _error("range", number_start)
        values[unit] = value

    return {
        "days": values["d"],
        "hours": values["h"],
        "minutes": values["m"],
        "seconds": values["s"],
        "milliseconds": values["ms"],
    }


def _decimal(value):
    if value == 0:
        return "0"
    chunks = []
    while value:
        value, remainder = divmod(value, 1_000_000_000)
        chunks.append(f"{remainder:09d}")
    return str(int(chunks[-1])) + "".join(reversed(chunks[:-1]))


def normalize_duration(text):
    fields = _scan(text)
    total_milliseconds = sum(
        value * _UNIT_MILLISECONDS[unit]
        for unit, value, _number_start, _unit_start in fields
    )

    days, remainder = divmod(total_milliseconds, _UNIT_MILLISECONDS["d"])
    hours, remainder = divmod(remainder, _UNIT_MILLISECONDS["h"])
    minutes, remainder = divmod(remainder, _UNIT_MILLISECONDS["m"])
    seconds, milliseconds = divmod(remainder, _UNIT_MILLISECONDS["s"])

    parts = []
    for value, unit in (
        (days, "d"),
        (hours, "h"),
        (minutes, "m"),
        (seconds, "s"),
        (milliseconds, "ms"),
    ):
        if value:
            parts.append(_decimal(value) + unit)

    return "".join(parts) if parts else "0s"
