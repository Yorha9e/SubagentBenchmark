"""Implement the public contract from TASKS.md."""

import copy


class _DeleteSentinel:
    def __repr__(self):
        return "DELETE"

    def __deepcopy__(self, memo):
        return self


DELETE = _DeleteSentinel()


def _is_plain_dict(value):
    return type(value) is dict


def apply_patch(base, patch, delete=DELETE):
    if not _is_plain_dict(base):
        raise TypeError("base must be a plain dict")
    if not _is_plain_dict(patch):
        raise TypeError("patch must be a plain dict")

    result = copy.deepcopy(base)

    for key, patch_value in patch.items():
        if patch_value is delete:
            result.pop(key, None)
            continue

        if key in result and _is_plain_dict(result[key]) and _is_plain_dict(patch_value):
            result[key] = apply_patch(result[key], patch_value, delete=delete)
        else:
            result[key] = copy.deepcopy(patch_value)

    return result
