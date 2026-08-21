"""Implement the public contract from TASKS.md."""

DELETE = object()


def _detach(value):
    """Return a deep copy of mutable containers; immutable values as-is."""
    if type(value) is dict:
        return {k: _detach(v) for k, v in value.items()}
    if type(value) is list:
        return [_detach(v) for v in value]
    return value


def apply_patch(base, patch, delete=DELETE):
    if type(base) is not dict or type(patch) is not dict:
        raise TypeError("base and patch must be plain dict instances")

    result = {}

    # Retain base keys in their original order.
    for key, old in base.items():
        if key in patch:
            new = patch[key]
            if new is delete:
                continue
            if type(old) is dict and type(new) is dict:
                result[key] = apply_patch(old, new, delete)
            else:
                result[key] = _detach(new)
        else:
            result[key] = _detach(old)

    # Append genuinely new keys in patch encounter order.
    for key, new in patch.items():
        if key in base:
            continue
        if new is delete:
            continue
        result[key] = _detach(new)

    return result
