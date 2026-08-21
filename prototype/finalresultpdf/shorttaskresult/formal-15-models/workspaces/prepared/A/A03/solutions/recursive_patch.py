"""Implement the public contract from TASKS.md."""

import copy


DELETE = object()


def apply_patch(base, patch, delete=DELETE):
    """Recursively merge patch into base, returning a fully detached result.

    Both base and patch must be plain dict objects (not subclasses).
    A patch value equal to delete removes the key.
    Only recursive merge when both old and patch values are plain dicts;
    otherwise the entire value is replaced.
    """
    if type(base) is not dict:
        raise TypeError("base must be a plain dict")
    if type(patch) is not dict:
        raise TypeError("patch must be a plain dict")

    result = {}

    # Preserve base key order: retained keys stay in their original positions.
    for k, v in base.items():
        if k in patch:
            pv = patch[k]
            if pv is delete:
                continue  # deletion
            if type(v) is dict and type(pv) is dict:
                result[k] = apply_patch(v, pv, delete)
            else:
                # Replace entirely; deep copy to avoid aliasing the patch input.
                result[k] = copy.deepcopy(pv)
        else:
            # Retain base value; deep copy to detach from input.
            result[k] = copy.deepcopy(v)

    # Append genuinely new keys in patch encounter order.
    for k, v in patch.items():
        if k not in base:
            if v is not delete:
                result[k] = copy.deepcopy(v)

    return result
