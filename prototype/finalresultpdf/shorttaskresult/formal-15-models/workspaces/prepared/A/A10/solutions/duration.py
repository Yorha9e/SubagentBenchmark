"""Implement the public contract from TASKS.md."""


class DurationParseError(ValueError):
    def __init__(self, code, position):
        self.code = code
        self.position = position
        super().__init__(f"Duration parse error: {code} at position {position}")


# Unit definitions in strict order
UNITS = [
    ("d", "days"),
    ("h", "hours"),
    ("m", "minutes"),
    ("s", "seconds"),
    ("ms", "milliseconds"),
]
UNIT_ORDER = {unit: i for i, (unit, _) in enumerate(UNITS)}
UNIT_TO_KEY = {unit: key for unit, key in UNITS}
MAX_SUBORDINATE = {
    "h": 24,
    "m": 60,
    "s": 60,
    "ms": 1000,
}


def parse_duration(text):
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if not text:
        raise DurationParseError("empty", 0)
    
    result = {
        "days": 0,
        "hours": 0,
        "minutes": 0,
        "seconds": 0,
        "milliseconds": 0,
    }
    seen_units = set()
    last_unit_idx = -1
    pos = 0
    
    while pos < len(text):
        # Parse digits
        start = pos
        while pos < len(text) and text[pos].isdigit():
            pos += 1
        if start == pos:
            raise DurationParseError("syntax", start)
        
        digits = text[start:pos]
        
        # Check leading zero
        if len(digits) > 1 and digits.startswith("0"):
            raise DurationParseError("leading_zero", start)
        
        # Parse unit
        unit_start = pos
        # Try two-character unit first (ms)
        if pos + 1 < len(text) and text[pos:pos+2] in UNIT_ORDER:
            unit = text[pos:pos+2]
            pos += 2
        elif pos < len(text) and text[pos] in UNIT_ORDER:
            unit = text[pos]
            pos += 1
        else:
            raise DurationParseError("syntax", unit_start)
        
        # Check unit order
        current_idx = UNIT_ORDER[unit]
        if current_idx <= last_unit_idx:
            raise DurationParseError("order", unit_start)
        last_unit_idx = current_idx
        
        # Check duplicate unit
        if unit in seen_units:
            raise DurationParseError("order", unit_start)  # Use order code for duplicates
        seen_units.add(unit)
        
        # Parse value
        value = int(digits)
        
        # Check range for subordinate units (parse only)
        if unit in MAX_SUBORDINATE and value >= MAX_SUBORDINATE[unit]:
            raise DurationParseError("range", start)
        
        result[UNIT_TO_KEY[unit]] = value
    
    if not seen_units:
        raise DurationParseError("empty", 0)
    
    return result


def normalize_duration(text):
    if not isinstance(text, str):
        raise DurationParseError("type", 0)
    if not text:
        raise DurationParseError("empty", 0)
    
    # First parse syntactically without strict range check
    total_ms = 0
    seen_units = set()
    last_unit_idx = -1
    pos = 0
    
    while pos < len(text):
        # Parse digits
        start = pos
        while pos < len(text) and text[pos].isdigit():
            pos += 1
        if start == pos:
            raise DurationParseError("syntax", start)
        
        digits = text[start:pos]
        
        # Check leading zero
        if len(digits) > 1 and digits.startswith("0"):
            raise DurationParseError("leading_zero", start)
        
        # Parse unit
        unit_start = pos
        if pos + 1 < len(text) and text[pos:pos+2] in UNIT_ORDER:
            unit = text[pos:pos+2]
            pos += 2
        elif pos < len(text) and text[pos] in UNIT_ORDER:
            unit = text[pos]
            pos += 1
        else:
            raise DurationParseError("syntax", unit_start)
        
        # Check unit order
        current_idx = UNIT_ORDER[unit]
        if current_idx <= last_unit_idx:
            raise DurationParseError("order", unit_start)
        last_unit_idx = current_idx
        
        # Check duplicate unit
        if unit in seen_units:
            raise DurationParseError("order", unit_start)
        seen_units.add(unit)
        
        value = int(digits)
        
        # Accumulate in milliseconds
        if unit == "d":
            total_ms += value * 24 * 60 * 60 * 1000
        elif unit == "h":
            total_ms += value * 60 * 60 * 1000
        elif unit == "m":
            total_ms += value * 60 * 1000
        elif unit == "s":
            total_ms += value * 1000
        elif unit == "ms":
            total_ms += value
    
    if not seen_units:
        raise DurationParseError("empty", 0)
    
    if total_ms == 0:
        return "0s"
    
    # Now build normalized output
    parts = []
    remaining = total_ms
    
    # Days
    if remaining >= 24 * 60 * 60 * 1000:
        days = remaining // (24 * 60 * 60 * 1000)
        parts.append(f"{days}d")
        remaining %= 24 * 60 * 60 * 1000
    
    # Hours
    if remaining >= 60 * 60 * 1000:
        hours = remaining // (60 * 60 * 1000)
        parts.append(f"{hours}h")
        remaining %= 60 * 60 * 1000
    
    # Minutes
    if remaining >= 60 * 1000:
        minutes = remaining // (60 * 1000)
        parts.append(f"{minutes}m")
        remaining %= 60 * 1000
    
    # Seconds
    if remaining >= 1000:
        seconds = remaining // 1000
        parts.append(f"{seconds}s")
        remaining %= 1000
    
    # Milliseconds
    if remaining > 0:
        parts.append(f"{remaining}ms")
    
    return "".join(parts)
