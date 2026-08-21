"""Implement the public contract from TASKS.md."""


# Unit-order indices for strict descending validation (d > h > m > s > ms).
_UNIT_ORDER = {"d": 0, "h": 1, "m": 2, "s": 3, "ms": 4}

# Multiplier for each unit → milliseconds.
_UNIT_MS = {
    "d": 24 * 60 * 60 * 1000,
    "h": 60 * 60 * 1000,
    "m": 60 * 1000,
    "s": 1000,
    "ms": 1,
}


class DurationParseError(ValueError):
    """Raised when duration text cannot be parsed."""

    def __init__(self, message, code, position):
        super().__init__(message)
        self.code = code
        self.position = position


def _parse_fields(text):
    """Yield (value, unit, start_index, end_index) tuples from *text*."""
    if not isinstance(text, str):
        raise DurationParseError("Duration must be a string", code="type", position=0)
    if len(text) == 0:
        raise DurationParseError("Duration cannot be empty", code="empty", position=0)

    fields = []
    i = 0
    n = len(text)
    while i < n:
        # --- digits ---
        if not text[i].isdigit():
            raise DurationParseError(
                "Expected digit", code="syntax", position=i
            )
        j = i
        while j < n and text[j].isdigit():
            j += 1
        digits = text[i:j]
        if len(digits) > 1 and digits[0] == "0":
            raise DurationParseError(
                "No leading zeros allowed",
                code="leading_zero",
                position=i,
            )
        value = int(digits)

        # --- unit ---
        if j >= n:
            raise DurationParseError(
                "Expected unit after digits", code="syntax", position=j
            )
        if j + 1 < n and text[j : j + 2] == "ms":
            unit = "ms"
            j += 2
        elif text[j] in "dhms":
            unit = text[j]
            j += 1
        else:
            raise DurationParseError(
                "Invalid unit", code="syntax", position=j
            )

        fields.append((value, unit, i, j))
        i = j

    if not fields:
        raise DurationParseError("No fields found", code="syntax", position=0)

    return fields


def _validate_order(fields):
    """Ensure units are in strict descending order with no repeats."""
    seen_units = set()
    prev_order = -1
    for value, unit, start, end in fields:
        if unit in seen_units:
            raise DurationParseError(
                f"Duplicate unit '{unit}'", code="order", position=start
            )
        seen_units.add(unit)
        curr_order = _UNIT_ORDER[unit]
        if curr_order <= prev_order:
            raise DurationParseError(
                "Units must be in strict descending order",
                code="order",
                position=start,
            )
        prev_order = curr_order


def _to_ms(fields):
    """Convert parsed fields to total milliseconds."""
    total = 0
    for value, unit, _s, _e in fields:
        total += value * _UNIT_MS[unit]
    return total


def _validate_ranges(fields):
    """Enforce subordinate range limits (parse_duration only)."""
    for value, unit, start, _end in fields:
        if unit == "h" and value >= 24:
            raise DurationParseError(
                "Hours must be less than 24", code="range", position=start
            )
        if unit == "m" and value >= 60:
            raise DurationParseError(
                "Minutes must be less than 60", code="range", position=start
            )
        if unit == "s" and value >= 60:
            raise DurationParseError(
                "Seconds must be less than 60", code="range", position=start
            )
        if unit == "ms" and value >= 1000:
            raise DurationParseError(
                "Milliseconds must be less than 1000",
                code="range",
                position=start,
            )


def parse_duration(text):
    """Parse *text* into a dict with keys days/hours/minutes/seconds/milliseconds.

    Subordinate ranges are enforced (h<24, m<60, s<60, ms<1000).
    """
    fields = _parse_fields(text)
    _validate_order(fields)
    _validate_ranges(fields)

    result = {
        "days": 0,
        "hours": 0,
        "minutes": 0,
        "seconds": 0,
        "milliseconds": 0,
    }
    for value, unit, _s, _e in fields:
        if unit == "d":
            result["days"] = value
        elif unit == "h":
            result["hours"] = value
        elif unit == "m":
            result["minutes"] = value
        elif unit == "s":
            result["seconds"] = value
        elif unit == "ms":
            result["milliseconds"] = value
    return result


def normalize_duration(text):
    """Parse *text* and convert to the shortest canonical equivalent.

    Out-of-range subordinate fields are accepted and normalised by carrying
    overflow into larger units.  Zero fields are omitted; canonical zero is
    ``"0s"``.  Normalization is idempotent.
    """
    fields = _parse_fields(text)
    _validate_order(fields)
    # No range validation — all numeric values are accepted.

    total_ms = _to_ms(fields)

    if total_ms == 0:
        return "0s"

    ms = total_ms % 1000
    total_s = total_ms // 1000
    s = total_s % 60
    total_m = total_s // 60
    m = total_m % 60
    total_h = total_m // 60
    h = total_h % 24
    d = total_h // 24

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
    if not parts:
        return "0s"
    return "".join(parts)
