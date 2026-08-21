"""Implement the public contract from TASKS.md."""

UNIT_SUFFIXES = (
    ("ms", "milliseconds", 1000),
    ("s", "seconds", 60),
    ("m", "minutes", 60),
    ("h", "hours", 24),
    ("d", "days", None),
)

UNIT_ORDER = {"d": 0, "h": 1, "m": 2, "s": 3, "ms": 4}
KEY_ORDER = ("days", "hours", "minutes", "seconds", "milliseconds")
SUFFIX_BY_KEY = {
    "days": "d",
    "hours": "h",
    "minutes": "m",
    "seconds": "s",
    "milliseconds": "ms",
}


class DurationParseError(ValueError):
    def __init__(self, code, position):
        self.code = code
        self.position = position
        super().__init__(f"{code} at position {position}")


def _match_unit(text, pos):
    for suffix, _, _ in UNIT_SUFFIXES:
        end = pos + len(suffix)
        if text[pos:end] == suffix:
            return suffix, end
    return None, pos


def _parse_duration_text(text, check_range):
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if text == "":
        raise DurationParseError("empty", 0)

    values = {key: 0 for key in KEY_ORDER}
    pos = 0
    last_unit_order = -1
    seen_units = set()

    while pos < len(text):
        start = pos
        if not text[pos].isdigit():
            raise DurationParseError("syntax", pos)

        digit_start = pos
        while pos < len(text) and text[pos].isdigit():
            pos += 1

        digits = text[digit_start:pos]
        if len(digits) > 1 and digits[0] == "0":
            raise DurationParseError("leading_zero", digit_start)

        unit, pos = _match_unit(text, pos)
        if unit is None:
            raise DurationParseError("syntax", pos)

        unit_order = UNIT_ORDER[unit]
        if unit_order <= last_unit_order or unit in seen_units:
            raise DurationParseError("order", start)

        seen_units.add(unit)
        last_unit_order = unit_order
        number = int(digits)

        if check_range:
            if unit == "h" and number >= 24:
                raise DurationParseError("range", digit_start)
            if unit == "m" and number >= 60:
                raise DurationParseError("range", digit_start)
            if unit == "s" and number >= 60:
                raise DurationParseError("range", digit_start)
            if unit == "ms" and number >= 1000:
                raise DurationParseError("range", digit_start)

        key = KEY_ORDER[unit_order]
        values[key] = number

    return values


def parse_duration(text):
    values = _parse_duration_text(text, check_range=True)
    return {
        "days": values["days"],
        "hours": values["hours"],
        "minutes": values["minutes"],
        "seconds": values["seconds"],
        "milliseconds": values["milliseconds"],
    }


def _normalize_values(values):
    ms = values["milliseconds"]
    seconds = values["seconds"] + ms // 1000
    ms = ms % 1000

    minutes = values["minutes"] + seconds // 60
    seconds = seconds % 60

    hours = values["hours"] + minutes // 60
    minutes = minutes % 60

    days = values["days"] + hours // 24
    hours = hours % 24

    return {
        "days": days,
        "hours": hours,
        "minutes": minutes,
        "seconds": seconds,
        "milliseconds": ms,
    }


def _format_duration(values):
    normalized = _normalize_values(values)
    parts = []
    for key in KEY_ORDER:
        amount = normalized[key]
        if amount:
            parts.append(f"{amount}{SUFFIX_BY_KEY[key]}")
    if not parts:
        return "0s"
    return "".join(parts)


def normalize_duration(text):
    values = _parse_duration_text(text, check_range=False)
    return _format_duration(values)
