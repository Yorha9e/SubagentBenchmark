"""Implement the public contract from TASKS.md."""


DELETE = object()


def _detach(value):
    if isinstance(value, dict):
        return {k: _detach(v) for k, v in value.items()}
    if isinstance(value, list):
        return [_detach(v) for v in value]
    if isinstance(value, set):
        return {_detach(v) for v in value}
    if isinstance(value, tuple):
        return tuple(_detach(v) for v in value)
    return value


def apply_patch(base, patch, delete=DELETE):
    if type(base) is not dict:
        raise TypeError("base must be a plain dict")
    if type(patch) is not dict:
        raise TypeError("patch must be a plain dict")

    result = {}

    # First, walk base in order; merge or detach.
    for key in base:
        if key in patch:
            patch_val = patch[key]
            if patch_val is delete:
                continue
            base_val = base[key]
            if type(base_val) is dict and type(patch_val) is dict:
                result[key] = apply_patch(base_val, patch_val, delete)
            else:
                result[key] = _detach(patch_val)
        else:
            base_val = base[key]
            if type(base_val) is dict:
                result[key] = _detach(base_val)
            else:
                result[key] = base_val

    # Then, append keys only in patch, in patch encounter order.
    for key in patch:
        if key in base:
            continue
        patch_val = patch[key]
        if patch_val is delete:
            continue
        result[key] = _detach(patch_val)

    return result
