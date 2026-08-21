"""Implement the public contract from TASKS.md."""


class DurationParseError(ValueError):
    """Raised for invalid duration input with a stable ``code``/``position``."""

    def __init__(self, code, position, message=None):
        self.code = code
        self.position = position
        if message is None:
            message = "{} at position {}".format(code, position)
        super().__init__(message)


# Strict descending unit order: d, h, m, s, ms.
_RANK_D = 0
_RANK_H = 1
_RANK_M = 2
_RANK_S = 3
_RANK_MS = 4

# Subordinate parse limits (exclusive upper bound); days are unbounded.
_LIMITS = {_RANK_H: 24, _RANK_M: 60, _RANK_S: 60, _RANK_MS: 1000}

# Milliseconds per unit, used for normalization.
_MS_PER_UNIT = {
    _RANK_D: 86400000,
    _RANK_H: 3600000,
    _RANK_M: 60000,
    _RANK_S: 1000,
    _RANK_MS: 1,
}

_KEY_BY_RANK = {
    _RANK_D: "days",
    _RANK_H: "hours",
    _RANK_M: "minutes",
    _RANK_S: "seconds",
    _RANK_MS: "milliseconds",
}


def _scan(text):
    """Left-to-right scan shared by parse_duration and normalize_duration.

    Returns a list of ``(value, rank, digit_start, unit_start)`` fields.
    Raises ``DurationParseError`` for type/empty/syntax/leading_zero/order
    problems but never for out-of-range subordinate values.
    """
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if text == "":
        raise DurationParseError("empty", 0)

    fields = []
    last_rank = -1
    i = 0
    n = len(text)
    while i < n:
        digit_start = i
        if not ("0" <= text[i] <= "9"):
            raise DurationParseError("syntax", i)
        j = i
        while j < n and "0" <= text[j] <= "9":
            j += 1
        number_text = text[i:j]
        if len(number_text) > 1 and number_text[0] == "0":
            raise DurationParseError("leading_zero", digit_start)
        value = int(number_text)
        i = j

        unit_start = i
        if i >= n:
            raise DurationParseError("syntax", unit_start)
        if text[i:i + 2] == "ms":
            rank = _RANK_MS
            i += 2
        elif text[i] == "d":
            rank = _RANK_D
            i += 1
        elif text[i] == "h":
            rank = _RANK_H
            i += 1
        elif text[i] == "m":
            rank = _RANK_M
            i += 1
        elif text[i] == "s":
            rank = _RANK_S
            i += 1
        else:
            raise DurationParseError("syntax", unit_start)

        if rank <= last_rank:
            raise DurationParseError("order", unit_start)
        last_rank = rank
        fields.append((value, rank, digit_start, unit_start))

    return fields


def parse_duration(text):
    fields = _scan(text)
    for value, rank, digit_start, _unit_start in fields:
        limit = _LIMITS.get(rank)
        if limit is not None and value >= limit:
            raise DurationParseError("range", digit_start)

    result = {
        "days": 0,
        "hours": 0,
        "minutes": 0,
        "seconds": 0,
        "milliseconds": 0,
    }
    for value, rank, _digit_start, _unit_start in fields:
        result[_KEY_BY_RANK[rank]] = value
    return result


def normalize_duration(text):
    fields = _scan(text)

    total = 0
    for value, rank, _digit_start, _unit_start in fields:
        total += value * _MS_PER_UNIT[rank]

    days, rem = divmod(total, 86400000)
    hours, rem = divmod(rem, 3600000)
    minutes, rem = divmod(rem, 60000)
    seconds, milliseconds = divmod(rem, 1000)

    parts = []
    if days:
        parts.append("{}d".format(days))
    if hours:
        parts.append("{}h".format(hours))
    if minutes:
        parts.append("{}m".format(minutes))
    if seconds:
        parts.append("{}s".format(seconds))
    if milliseconds:
        parts.append("{}ms".format(milliseconds))
    if not parts:
        return "0s"
    return "".join(parts)
