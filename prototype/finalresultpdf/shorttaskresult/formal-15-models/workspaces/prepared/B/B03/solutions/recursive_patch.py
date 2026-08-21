"""Implement the public contract from TASKS.md."""

import copy


class _DeleteSentinel:
    """Unique sentinel whose identity triggers deletions."""

    def __deepcopy__(self, memo):
        return self


DELETE = _DeleteSentinel()


def apply_patch(base, patch, delete=DELETE):
    """Recursively merge *patch* into *base*; a patch value *is* *delete* removes the key.

    Only plain ``dict`` (not subclasses) triggers recursive merging; every other
    value is replaced wholesale.  The return value is fully detached from both
    inputs via ``copy.deepcopy``.
    """
    if type(base) is not dict:
        raise TypeError("base must be a plain dict")
    if type(patch) is not dict:
        raise TypeError("patch must be a plain dict")

    result = copy.deepcopy(base)

    for key, patch_value in patch.items():
        if patch_value is delete:
            result.pop(key, None)
            continue

        if key in result and type(result[key]) is dict and type(patch_value) is dict:
            result[key] = apply_patch(result[key], patch_value, delete=delete)
        else:
            result[key] = copy.deepcopy(patch_value)

    return result
