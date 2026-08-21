"""Implement the public contract from TASKS.md."""

DELETE = object()


def _deep_copy(obj):
    if isinstance(obj, dict):
        return {k: _deep_copy(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_deep_copy(v) for v in obj]
    if isinstance(obj, tuple):
        return tuple(_deep_copy(v) for v in obj)
    if isinstance(obj, set):
        return {_deep_copy(v) for v in obj}
    return obj


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
            if isinstance(bval, dict) and isinstance(pval, dict):
                result[key] = apply_patch(bval, pval, delete=delete)
            else:
                result[key] = _deep_copy(pval)
        else:
            result[key] = _deep_copy(base[key])
    for key in patch:
        if key not in base:
            pval = patch[key]
            if pval is not delete:
                result[key] = _deep_copy(pval)
    return result
