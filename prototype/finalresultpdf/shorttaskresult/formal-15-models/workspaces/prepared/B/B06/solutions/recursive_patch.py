"""Implement the public contract from TASKS.md."""

import copy


class _DeleteSentinel:
    """Unique sentinel marking a deletion in a patch mapping."""

    __slots__ = ()

    def __repr__(self):
        return "DELETE"

    def __deepcopy__(self, memo):
        # Keep a single public sentinel even when nested inside copied data.
        return self


DELETE = _DeleteSentinel()


def apply_patch(base, patch, delete=DELETE):
    if type(base) is not dict:
        raise TypeError("base must be a plain dict")
    if type(patch) is not dict:
        raise TypeError("patch must be a plain dict")
    return _merge(base, patch, delete)


def _merge(base, patch, delete):
    # A full deep copy of base detaches every retained branch and keeps the
    # original key order; assigning to an existing key preserves its position
    # while genuinely new keys are appended in patch encounter order.
    result = copy.deepcopy(base)
    for key, patch_value in patch.items():
        if patch_value is delete:
            result.pop(key, None)
            continue
        if key in result and type(result[key]) is dict and type(patch_value) is dict:
            result[key] = _merge(result[key], patch_value, delete)
        else:
            # Whole-value replacement: deep-copy so replacement branches are
            # detached from patch; a replacement dict keeps patch's own order.
            result[key] = copy.deepcopy(patch_value)
    return result
