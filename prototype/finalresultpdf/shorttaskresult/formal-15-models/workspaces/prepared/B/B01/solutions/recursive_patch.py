"""Implement the public contract from TASKS.md."""

import copy


class _DeleteType:
    """Unique sentinel marking a patch value as a deletion."""

    def __deepcopy__(self, memo):
        return self

    def __repr__(self):
        return "DELETE"


DELETE = _DeleteType()


def apply_patch(base, patch, delete=DELETE):
    if type(base) is not dict:
        raise TypeError("base must be a plain dict")
    if type(patch) is not dict:
        raise TypeError("patch must be a plain dict")
    result = copy.deepcopy(base)
    for key, patch_value in patch.items():
        if patch_value is delete:
            if key in result:
                del result[key]
            continue
        if key in result and type(result[key]) is dict and type(patch_value) is dict:
            result[key] = apply_patch(result[key], patch_value, delete=delete)
        else:
            result[key] = copy.deepcopy(patch_value)
    return result
