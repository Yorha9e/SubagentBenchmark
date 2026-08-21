"""Implement the public contract from TASKS.md."""

import copy

DELETE = object()


def _detach(value):
    t = type(value)
    if t is dict:
        return {key: _detach(item) for key, item in value.items()}
    if t is list:
        return [_detach(item) for item in value]
    if t is tuple:
        return tuple(_detach(item) for item in value)
    if t is set:
        return set(value)
    if t is frozenset:
        return value
    if isinstance(value, (dict, list, tuple, set)):
        return copy.deepcopy(value)
    return value


def _merge(base, patch, delete):
    result = {}
    for key, base_value in base.items():
        if key in patch:
            patch_value = patch[key]
            if patch_value is delete:
                continue
            if type(base_value) is dict and type(patch_value) is dict:
                result[key] = _merge(base_value, patch_value, delete)
            else:
                result[key] = _detach(patch_value)
        else:
            result[key] = _detach(base_value)
    for key, patch_value in patch.items():
        if key in base or patch_value is delete:
            continue
        result[key] = _detach(patch_value)
    return result


def apply_patch(base, patch, delete=DELETE):
    if type(base) is not dict or type(patch) is not dict:
        raise TypeError("base and patch must be plain dict objects")
    return _merge(base, patch, delete)
