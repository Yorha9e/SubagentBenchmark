"""Implement the public contract from TASKS.md."""

DELETE = object()


def _deep_copy(value):
    if type(value) is dict:
        return {k: _deep_copy(v) for k, v in value.items()}
    if type(value) is list:
        return [_deep_copy(item) for item in value]
    return value


def apply_patch(base, patch, delete=DELETE):
    result = {}

    for key in base:
        if key in patch:
            patch_val = patch[key]
            if patch_val is delete:
                continue
            base_val = base[key]
            if type(base_val) is dict and type(patch_val) is dict:
                result[key] = apply_patch(base_val, patch_val, delete=delete)
            else:
                result[key] = _deep_copy(patch_val)
        else:
            result[key] = _deep_copy(base[key])

    for key in patch:
        if key not in base:
            patch_val = patch[key]
            if patch_val is not delete:
                result[key] = _deep_copy(patch_val)

    return result
