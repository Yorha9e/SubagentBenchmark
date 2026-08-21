"""Recursive, detached dictionary patching."""

from copy import deepcopy


class _DeleteSentinel:
    __slots__ = ()

    def __deepcopy__(self, memo):
        return self


DELETE = _DeleteSentinel()


def apply_patch(base, patch, delete=DELETE):
    """Apply a recursive dictionary patch without mutating either input."""
    if type(base) is not dict:
        raise TypeError("base must be a plain dict")
    if type(patch) is not dict:
        raise TypeError("patch must be a plain dict")

    memo = {}
    result = deepcopy(base, memo)

    def merge(target, patch_dict):
        for key, patch_value in patch_dict.items():
            if patch_value is delete:
                if key in target:
                    del target[key]
                continue

            if (
                key in target
                and type(target[key]) is dict
                and type(patch_value) is dict
            ):
                merge(target[key], patch_value)
            else:
                target[key] = deepcopy(patch_value, memo)

    merge(result, patch)
    return result
