"""Implement the public contract from TASKS.md."""

_UNIT_ORDER = ["d", "h", "m", "s", "ms"]
_UNIT_RANK = {u: i for i, u in enumerate(_UNIT_ORDER)}
_UNIT_TO_KEY = {
    "d": "days",
    "h": "hours",
    "m": "minutes",
    "s": "seconds",
    "ms": "milliseconds",
}
_UNIT_TO_MS = {"d": 86400000, "h": 3600000, "m": 60000, "s": 1000, "ms": 1}
_RANGE_LIMITS = {"h": 24, "m": 60, "s": 60, "ms": 1000}


class DurationParseError(ValueError):
    def __init__(self, code, position, message=""):
        super().__init__(message)
        self.code = code
        self.position = position


def _tokenize(text):
    """Tokenize duration text.

    Returns list of (value, unit, start_position).
    Raises DurationParseError on invalid input.
    """
    if not isinstance(text, str):
        raise DurationParseError("type", 0, "")

    if not text:
        raise DurationParseError("empty", 0, "")

    # Reject characters outside the grammar
    allowed = set("0123456789dhms")
    for pos, ch in enumerate(text):
        if ch not in allowed:
            raise DurationParseError("syntax", pos, "")

    i = 0
    n = len(text)
    tokens = []

    while i < n:
        num_start = i
        while i < n and text[i].isdigit():
            i += 1
        if i == num_start:
            raise DurationParseError("syntax", i, "")

        num_str = text[num_start:i]

        # Leading zero check: the value 0 is fine, "00", "01" etc. are not
        if len(num_str) > 1 and num_str[0] == "0":
            raise DurationParseError("leading_zero", num_start, "")

        value = int(num_str)

        # Read unit: prefer longest match (ms before m or s)
        unit = None
        if i + 1 < n and text[i : i + 2] == "ms":
            unit = "ms"
            i += 2
        elif i < n and text[i] in "dhms":
            unit = text[i]
            i += 1
        else:
            raise DurationParseError("syntax", i, "")

        tokens.append((value, unit, num_start))

    # Validate strict descending unit order (strictly increasing rank)
    for j in range(1, len(tokens)):
        if _UNIT_RANK[tokens[j][1]] <= _UNIT_RANK[tokens[j - 1][1]]:
            raise DurationParseError("order", tokens[j][2], "")

    return tokens


def parse_duration(text):
    tokens = _tokenize(text)

    result = {"days": 0, "hours": 0, "minutes": 0, "seconds": 0, "milliseconds": 0}

    for value, unit, pos in tokens:
        if unit != "d":
            limit = _RANGE_LIMITS[unit]
            if not (0 <= value < limit):
                raise DurationParseError("range", pos, "")
        result[_UNIT_TO_KEY[unit]] = value

    return result


def normalize_duration(text):
    tokens = _tokenize(text)

    total_ms = 0
    for value, unit, _ in tokens:
        total_ms += value * _UNIT_TO_MS[unit]

    days, r = divmod(total_ms, 86400000)
    hours, r = divmod(r, 3600000)
    minutes, r = divmod(r, 60000)
    seconds, milliseconds = divmod(r, 1000)

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

    if not parts:
        return "0s"

    return "".join(parts)
