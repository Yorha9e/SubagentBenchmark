"""Implement the public contract from TASKS.md."""

import copy

DELETE = object()


def apply_patch(base, patch, delete=DELETE):
    if type(base) is not dict or type(patch) is not dict:
        raise TypeError("base and patch must be plain dicts")

    result = {}
    for k, v in base.items():
        result[k] = copy.deepcopy(v)

    for k, v in patch.items():
        if v is delete:
            result.pop(k, None)
        elif k in result and type(result[k]) is dict and type(v) is dict:
            result[k] = apply_patch(result[k], v, delete)
        else:
            result[k] = copy.deepcopy(v)

    return result
