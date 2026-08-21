"""Implement the public contract from TASKS.md."""

OUTPUT_KEYS = ("days", "hours", "minutes", "seconds", "milliseconds")
UNIT_TO_KEY = {
    "d": "days",
    "h": "hours",
    "m": "minutes",
    "s": "seconds",
    "ms": "milliseconds",
}
UNIT_RANK = {"d": 0, "h": 1, "m": 2, "s": 3, "ms": 4}
PARSE_LIMITS = {"h": 24, "m": 60, "s": 60, "ms": 1000}

MS_PER_SECOND = 1000
MS_PER_MINUTE = 60 * MS_PER_SECOND
MS_PER_HOUR = 60 * MS_PER_MINUTE
MS_PER_DAY = 24 * MS_PER_HOUR


class DurationParseError(ValueError):
    def __init__(self, code, position, message=None):
        self.code = code
        self.position = position
        if message is None:
            message = f"{code} error at position {position}"
        super().__init__(message)


def _scan_fields(text, check_range):
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if text == "":
        raise DurationParseError("empty", 0)

    fields = []
    position = 0
    last_rank = -1

    while position < len(text):
        if not ("0" <= text[position] <= "9"):
            raise DurationParseError("syntax", position)

        number_start = position
        while position < len(text) and "0" <= text[position] <= "9":
            position += 1

        number_text = text[number_start:position]
        if len(number_text) > 1 and number_text[0] == "0":
            raise DurationParseError("leading_zero", number_start)

        value = int(number_text)
        unit_start = position

        if text[position : position + 2] == "ms":
            unit = "ms"
            position += 2
        elif position < len(text) and text[position] in "dhms":
            unit = text[position]
            position += 1
        else:
            raise DurationParseError("syntax", position)

        rank = UNIT_RANK[unit]
        if rank <= last_rank:
            raise DurationParseError("order", unit_start)
        last_rank = rank

        fields.append((unit, value, number_start))

    if check_range:
        for unit, value, number_start in fields:
            limit = PARSE_LIMITS.get(unit)
            if limit is not None and value >= limit:
                raise DurationParseError("range", number_start)

    return fields


def parse_duration(text):
    fields = _scan_fields(text, check_range=True)
    values = {key: 0 for key in OUTPUT_KEYS}
    for unit, value, _ in fields:
        values[UNIT_TO_KEY[unit]] = value
    return {key: values[key] for key in OUTPUT_KEYS}


def normalize_duration(text):
    fields = _scan_fields(text, check_range=False)

    total_ms = 0
    for unit, value, _ in fields:
        if unit == "d":
            total_ms += value * MS_PER_DAY
        elif unit == "h":
            total_ms += value * MS_PER_HOUR
        elif unit == "m":
            total_ms += value * MS_PER_MINUTE
        elif unit == "s":
            total_ms += value * MS_PER_SECOND
        else:
            total_ms += value

    if total_ms == 0:
        return "0s"

    days, remainder = divmod(total_ms, MS_PER_DAY)
    hours, remainder = divmod(remainder, MS_PER_HOUR)
    minutes, remainder = divmod(remainder, MS_PER_MINUTE)
    seconds, milliseconds = divmod(remainder, MS_PER_SECOND)

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
    return "".join(parts)
