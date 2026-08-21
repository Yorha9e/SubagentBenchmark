"""Implement the public contract from TASKS.md."""

DELETE = object()


def _detach(value):
    """Return a copy sharing no mutable container with the original."""
    if isinstance(value, dict):
        return {k: _detach(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_detach(v) for v in value]
    if isinstance(value, tuple):
        return tuple(_detach(v) for v in value)
    if isinstance(value, set):
        return {_detach(v) for v in value}
    if isinstance(value, bytearray):
        return bytearray(value)
    return value


def apply_patch(base, patch, delete=DELETE):
    if type(base) is not dict or type(patch) is not dict:
        raise TypeError("base and patch must be plain dict objects")
    result = {}
    for key in base:
        if key in patch:
            pval = patch[key]
            if pval is delete:
                continue
            bval = base[key]
            if type(bval) is dict and type(pval) is dict:
                result[key] = apply_patch(bval, pval, delete)
            else:
                result[key] = _detach(pval)
        else:
            result[key] = _detach(base[key])
    for key in patch:
        if key not in base:
            pval = patch[key]
            if pval is delete:
                continue
            result[key] = _detach(pval)
    return result
