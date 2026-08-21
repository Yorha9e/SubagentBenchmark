"""Implement the public contract from TASKS.md."""


class DurationParseError(ValueError):
    """Raised on invalid duration text, carrying a deterministic ``.code`` and ``.position``."""

    def __init__(self, code, position, message=""):
        self.code = code
        self.position = position
        detail = f" (pos {position})" if message else ""
        super().__init__(f"{code}{detail}" if not message else f"{code}: {message} (pos {position})")


# Unit metadata — kept in strict descending order
_UNIT_NAMES = ["d", "h", "m", "s", "ms"]
_UNIT_RANK = {"d": 0, "h": 1, "m": 2, "s": 3, "ms": 4}
_KEY_ORDER = ["days", "hours", "minutes", "seconds", "milliseconds"]
_KEY_MAP = {0: "days", 1: "hours", 2: "minutes", 3: "seconds", 4: "milliseconds"}

# Parse-only subordinate maxima (exclusive upper bound)
_PARSE_MAX = {1: 24, 2: 60, 3: 60, 4: 1000}

# Multipliers to convert each unit to milliseconds
_MS_MULT = {0: 86_400_000, 1: 3_600_000, 2: 60_000, 3: 1_000, 4: 1}


def _scan(text):
    """Shared scanner: left-to-right, strict grammar, no range checks.

    Returns list of ``(value, unit_rank, digit_start, unit_start)`` or raises
    ``DurationParseError`` with deterministic code and position.
    """
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if text == "":
        raise DurationParseError("empty", 0)

    pos = 0
    n = len(text)
    fields = []
    last_rank = -1  # nothing accepted yet

    while pos < n:
        digit_start = pos

        # ----- digits (at least one) -----
        if not ("0" <= text[pos] <= "9"):
            raise DurationParseError("syntax", pos)

        value = 0
        digit_count = 0
        while pos < n and "0" <= text[pos] <= "9":
            value = value * 10 + (ord(text[pos]) - ord("0"))
            digit_count += 1
            pos += 1

        # Leading zero on multi-digit field
        if digit_count > 1 and text[digit_start] == "0":
            raise DurationParseError("leading_zero", digit_start)

        # ----- unit (try "ms" first, then single-char) -----
        unit_start = pos
        if pos + 1 < n and text[pos : pos + 2] == "ms":
            unit = "ms"
            pos += 2
        elif pos < n and text[pos] in "dhms":
            unit = text[pos]
            pos += 1
        else:
            # Unexpected character or premature end
            raise DurationParseError("syntax", pos)

        rank = _UNIT_RANK[unit]
        if rank <= last_rank:
            raise DurationParseError("order", unit_start)
        last_rank = rank

        fields.append((value, rank, digit_start, unit_start))

    return fields


def parse_duration(text):
    """Parse *text* strictly and return ``{days, hours, minutes, seconds, milliseconds}``.

    Subordinate fields must be in range: ``h < 24, m < 60, s < 60, ms < 1000``.
    """
    fields = _scan(text)

    result = {"days": 0, "hours": 0, "minutes": 0, "seconds": 0, "milliseconds": 0}
    for value, rank, digit_start, _unit_start in fields:
        if rank in _PARSE_MAX and value >= _PARSE_MAX[rank]:
            raise DurationParseError("range", digit_start)
        result[_KEY_MAP[rank]] = value

    return result


def normalize_duration(text):
    """Parse *text* and return the shortest canonical equivalent string.

    Out-of-range subordinate fields are carried into larger units.
    Zero fields are omitted; the canonical zero representation is ``"0s"``.
    """
    fields = _scan(text)

    # Accumulate total milliseconds (Python int handles unbounded days)
    total_ms = 0
    for value, rank, _digit_start, _unit_start in fields:
        total_ms += value * _MS_MULT[rank]

    if total_ms == 0:
        return "0s"

    ms = total_ms % 1000
    total_sec = total_ms // 1000
    s = total_sec % 60
    total_min = total_sec // 60
    m = total_min % 60
    total_hour = total_min // 60
    h = total_hour % 24
    d = total_hour // 24

    parts = []
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
