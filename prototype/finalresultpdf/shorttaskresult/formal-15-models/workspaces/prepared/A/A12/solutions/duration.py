"""Parse and normalize human-readable duration strings.

Grammar: one or more adjacent ``<int><unit>`` fields in strict descending
unit order  ``d  h  m  s  ms``.  Fields cannot repeat, contain
whitespace / signs / decimals, or use leading zeroes (except the single
value ``0``).
"""

import re as _re

# Canonical key order required by parse_duration.
_KEYS = ("days", "hours", "minutes", "seconds", "milliseconds")

# Unit -> multiplier to convert to milliseconds.
_TO_MS = {"d": 86_400_000, "h": 3_600_000, "m": 60_000, "s": 1_000, "ms": 1}

# Descending order index for each unit.
_UNIT_ORDER = {"d": 0, "h": 1, "m": 2, "s": 3, "ms": 4}

_UNIT_KEY = {"d": "days", "h": "hours", "m": "minutes", "s": "seconds", "ms": "milliseconds"}


class DurationParseError(ValueError):
    """Raised for any duration string that cannot be parsed."""

    def __init__(self, code, position, message=""):
        self.code = code
        self.position = position
        super().__init__(message or f"DurationParseError({code!r}, pos={position})")


# ---------------------------------------------------------------------------
# Shared parser
# ---------------------------------------------------------------------------

def _parse_fields(text):
    """Parse *text* into a list of ``(unit, value, start_pos)`` tuples.

    Validates syntax, leading zeroes, and unit ordering but **not** range.
    """
    pos = 0
    length = len(text)
    fields = []
    prev_order = -1

    while pos < length:
        # --- number ---
        num_start = pos
        ch = text[pos]
        if ch == "0":
            pos += 1
            if pos < length and text[pos].isdigit():
                raise DurationParseError("leading_zero", num_start)
            num_str = "0"
        elif "1" <= ch <= "9":
            pos += 1
            while pos < length and text[pos].isdigit():
                pos += 1
            num_str = text[num_start:pos]
        else:
            raise DurationParseError("syntax", pos)

        value = int(num_str)

        # --- unit ---
        if pos + 1 <= length and text[pos:pos + 2] == "ms":
            unit = "ms"
            pos += 2
        elif pos < length and text[pos] in "dhms":
            unit = text[pos]
            pos += 1
        else:
            raise DurationParseError("syntax", pos)

        # --- ordering ---
        uo = _UNIT_ORDER[unit]
        if uo <= prev_order:
            raise DurationParseError("order", num_start)
        prev_order = uo

        fields.append((unit, value, num_start))

    return fields


# ---------------------------------------------------------------------------
# parse_duration
# ---------------------------------------------------------------------------

def parse_duration(text):
    """Parse *text* and return a dict with keys
    ``days, hours, minutes, seconds, milliseconds`` (all present).

    Subordinate units are range-checked (h<24, m<60, s<60, ms<1000).
    """
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if not text:
        raise DurationParseError("empty", 0)

    fields = _parse_fields(text)

    result = {k: 0 for k in _KEYS}
    for unit, value, pos in fields:
        result[_UNIT_KEY[unit]] = value
        # Range check for subordinate units.
        if unit == "h" and value >= 24:
            raise DurationParseError("range", pos)
        if unit == "m" and value >= 60:
            raise DurationParseError("range", pos)
        if unit == "s" and value >= 60:
            raise DurationParseError("range", pos)
        if unit == "ms" and value >= 1000:
            raise DurationParseError("range", pos)

    return result


# ---------------------------------------------------------------------------
# normalize_duration
# ---------------------------------------------------------------------------

def normalize_duration(text):
    """Accept a syntactically valid duration (subordinate overflow OK) and
    return the shortest canonical equivalent string.

    Zero fields are omitted; the canonical zero is ``0s``.
    Normalization is idempotent.
    """
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if not text:
        raise DurationParseError("empty", 0)

    fields = _parse_fields(text)

    # Convert everything to milliseconds.
    total_ms = 0
    for unit, value, _pos in fields:
        total_ms += value * _TO_MS[unit]

    if total_ms == 0:
        return "0s"

    # Decompose into canonical descending fields.
    parts = []
    for unit in ("d", "h", "m", "s", "ms"):
        factor = _TO_MS[unit]
        qty, total_ms = divmod(total_ms, factor)
        if qty:
            parts.append(f"{qty}{unit}")

    return "".join(parts)
