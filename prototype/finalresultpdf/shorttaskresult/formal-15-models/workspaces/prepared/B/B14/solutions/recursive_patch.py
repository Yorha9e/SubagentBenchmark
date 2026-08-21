"""Implement the public contract from TASKS.md."""

import copy


class _DeleteType:
    """Unique module-level deletion sentinel.

    ``__deepcopy__`` returns ``self`` so deep-copying nested data never
    produces a second public sentinel object.
    """

    def __deepcopy__(self, memo):
        return self

    def __repr__(self):
        return "<DELETE>"


DELETE = _DeleteType()


def _merge(target, patch, delete):
    for key, patch_value in patch.items():
        if patch_value is delete:
            if key in target:
                del target[key]
            continue
        if key in target and type(target[key]) is dict and type(patch_value) is dict:
            _merge(target[key], patch_value, delete)
        else:
            target[key] = copy.deepcopy(patch_value)
    return target


def apply_patch(base, patch, delete=DELETE):
    if type(base) is not dict:
        raise TypeError("base must be a plain dict")
    if type(patch) is not dict:
        raise TypeError("patch must be a plain dict")
    result = copy.deepcopy(base)
    return _merge(result, patch, delete)
