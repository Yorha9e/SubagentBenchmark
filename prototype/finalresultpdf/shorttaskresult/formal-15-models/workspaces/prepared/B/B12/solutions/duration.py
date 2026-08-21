"""Duration string parsing and normalization."""


class DurationParseError(ValueError):
    """Raised for invalid duration strings."""

    def __init__(self, code, position, message=""):
        self.code = code
        self.position = position
        super().__init__(message or f"duration parse error ({code}) at position {position}")


# Fixed metadata
_UNIT_ORDER = ["d", "h", "m", "s", "ms"]
_UNIT_RANK = {u: i for i, u in enumerate(_UNIT_ORDER)}
_OUT_KEYS = ["days", "hours", "minutes", "seconds", "milliseconds"]
_RANGES = {"h": 24, "m": 60, "s": 60, "ms": 1000}  # subordinate upper bounds (exclusive)
_MS_PER = {"d": 86400000, "h": 3600000, "m": 60000, "s": 1000, "ms": 1}
_OUT_KEY_MAP = {"d": "days", "h": "hours", "m": "minutes", "s": "seconds", "ms": "milliseconds"}


def _raise(code, pos, msg=""):
    raise DurationParseError(code, pos, msg)


def _scan(text):
    """Shared left-to-right scanner.

    Returns a list of ``(unit, value, digit_start, unit_start)`` tuples.

    Raises ``DurationParseError`` for any syntax/order/leading-zero violation.
    """
    if not isinstance(text, str):
        _raise("type", 0, "expected a string")

    if len(text) == 0:
        _raise("empty", 0, "empty duration string")

    pos = 0
    length = len(text)
    fields = []
    last_rank = -1  # enforce strict descending unit order

    while pos < length:
        # ---- read digits ----
        digit_start = pos
        if pos >= length or not ('0' <= text[pos] <= '9'):
            _raise("syntax", pos, f"expected digit at position {pos}")

        while pos < length and '0' <= text[pos] <= '9':
            pos += 1

        num_str = text[digit_start:pos]

        # Leading zero check: multi-digit number starting with '0'
        if len(num_str) > 1 and num_str[0] == '0':
            _raise("leading_zero", digit_start, "leading zero not allowed")

        value = int(num_str)

        # ---- read unit ----
        unit_start = pos
        if pos >= length:
            _raise("syntax", pos, "expected unit after digits")

        unit = None
        # Try 'ms' first (two chars)
        if pos + 1 < length and text[pos:pos + 2] == "ms":
            unit = "ms"
            pos += 2
        elif text[pos] in ("d", "h", "m", "s"):
            unit = text[pos]
            pos += 1
        else:
            _raise("syntax", unit_start, f"unexpected character at position {unit_start}")

        # Check for trailing garbage is implicit – next iteration will fail on
        # missing digits if there's junk between fields.

        rank = _UNIT_RANK[unit]
        if rank <= last_rank:
            _raise("order", unit_start, "units must be in strict descending order")
        last_rank = rank

        fields.append((unit, value, digit_start, unit_start))

    return fields


def _check_ranges(fields):
    """Range-check subordinate fields for parse_duration."""
    for unit, value, digit_start, _ in fields:
        limit = _RANGES.get(unit)
        if limit is not None and value >= limit:
            _raise("range", digit_start,
                   f"{unit} value {value} out of range (must be < {limit})")


def parse_duration(text):
    """Parse a duration string into a dict with fixed key order.

    Subordinate fields must be in range (h<24, m<60, s<60, ms<1000).
    Returns ``{"days": …, "hours": …, "minutes": …, "seconds": …, "milliseconds": …}``.
    """
    fields = _scan(text)
    _check_ranges(fields)

    result = {k: 0 for k in _OUT_KEYS}
    for unit, value, _, _ in fields:
        result[_OUT_KEY_MAP[unit]] = value
    return result


def normalize_duration(text):
    """Parse and normalize a duration to canonical form.

    Accepts syntactically valid out-of-range subordinate fields and carries
    overflow into larger units.  Omitting zero fields except canonical zero
    is ``"0s"``.  Normalization is idempotent.
    """
    fields = _scan(text)
    # No range check for normalize – overflow is handled via carry

    total_ms = 0
    for unit, value, _, _ in fields:
        total_ms += value * _MS_PER[unit]

    if total_ms == 0:
        return "0s"

    parts = []
    for unit in ("d", "h", "m", "s", "ms"):
        if total_ms >= _MS_PER[unit]:
            count, total_ms = divmod(total_ms, _MS_PER[unit])
            parts.append(f"{count}{unit}")

    return "".join(parts)
