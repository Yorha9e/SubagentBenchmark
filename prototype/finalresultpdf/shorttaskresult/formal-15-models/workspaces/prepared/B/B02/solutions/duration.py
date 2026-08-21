"""Implement the public contract from TASKS.md."""

_UNITS = [
    ("d", 0, 86_400_000),  # days -> ms
    ("h", 1, 3_600_000),   # hours -> ms
    ("m", 2, 60_000),      # minutes -> ms
    ("s", 3, 1_000),       # seconds -> ms
    ("ms", 4, 1),          # milliseconds -> ms
]

_OUTPUT_KEYS = ["days", "hours", "minutes", "seconds", "milliseconds"]

_PARSE_MAX = {1: 23, 2: 59, 3: 59, 4: 999}  # rank -> max; day rank 0 is unbounded


class DurationParseError(ValueError):
    def __init__(self, code, position, msg=""):
        self.code = code
        self.position = position
        super().__init__(msg or f"{code} at {position}")


def _scan(text):
    """Shared scanner returning a list of (rank, value, digit_start, unit_start).

    Raises DurationParseError for syntax/leading_zero/order errors.
    """
    if not isinstance(text, str):
        raise DurationParseError("type", 0)

    n = len(text)
    if n == 0:
        raise DurationParseError("empty", 0)

    pos = 0
    prev_rank = -1
    fields = []  # (rank, value, digit_start, unit_start)

    while pos < n:
        # read digit sequence
        digit_start = pos
        if not ("0" <= text[pos] <= "9"):
            raise DurationParseError("syntax", pos)
        while pos < n and "0" <= text[pos] <= "9":
            pos += 1
        # now pos is at the start of the unit (or end)
        digit_len = pos - digit_start

        # leading zero check
        if digit_len > 1 and text[digit_start] == "0":
            raise DurationParseError("leading_zero", digit_start)

        value = int(text[digit_start:pos])

        if pos >= n:
            raise DurationParseError("syntax", n)

        # read unit – try "ms" first
        unit_start = pos
        if pos + 1 < n and text[pos:pos+2] == "ms":
            unit = "ms"
            pos += 2
        elif text[pos] in "dhms":
            unit = text[pos]
            pos += 1
        else:
            raise DurationParseError("syntax", unit_start)

        # find rank
        rank = None
        for u, r, _ in _UNITS:
            if u == unit:
                rank = r
                break

        if rank <= prev_rank:
            raise DurationParseError("order", unit_start)
        prev_rank = rank

        fields.append((rank, value, digit_start, unit_start))

    # After the loop
    if not fields:
        # This shouldn't happen if n > 0 and we didn't error, but just in case
        raise DurationParseError("syntax", 0)

    return fields


def _fields_to_dict(fields):
    """Convert scanned fields to a fixed-order dict with all keys."""
    result = {k: 0 for k in _OUTPUT_KEYS}
    for rank, value, _, _ in fields:
        result[_OUTPUT_KEYS[rank]] = value
    return result


def parse_duration(text):
    fields = _scan(text)

    # Range check on subordinate fields
    for rank, value, digit_start, _ in fields:
        max_val = _PARSE_MAX.get(rank)
        if max_val is not None and value > max_val:
            raise DurationParseError("range", digit_start)

    return _fields_to_dict(fields)


def normalize_duration(text):
    fields = _scan(text)

    # No range check – accept any valid syntax, carry overflow
    total_ms = 0
    for rank, value, _, _ in fields:
        _, _, factor = _UNITS[rank]
        total_ms += value * factor

    # Carry overflow into larger units
    carrier = [
        ("ms", 4, 1),
        ("s", 3, 1000),
        ("m", 2, 60),
        ("h", 1, 60),
        ("d", 0, 24),
    ]

    ms = total_ms
    s, ms = divmod(ms, 1000)
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    d, h = divmod(h, 24)

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

    return "".join(parts) if parts else "0s"
