import copy

DELETE = object()


def apply_patch(base, patch, delete=DELETE):
    """Recursively merge *patch* into *base*, returning a fully detached result.

    A patch value that *is* ``delete`` removes the corresponding key.
    Recurse only where both old and patch values are plain dicts; otherwise
    replace the entire value.  The result shares no mutable container with
    either input, and the inputs are left unchanged.
    """
    if type(base) is not dict:
        raise TypeError("base must be a plain dict")
    if type(patch) is not dict:
        raise TypeError("patch must be a plain dict")

    result = {}
    # Retained base keys keep their positions; new keys follow patch order.
    for key in base:
        if key in patch:
            patch_val = patch[key]
            if patch_val is delete:
                continue
            base_val = base[key]
            if type(base_val) is dict and type(patch_val) is dict:
                result[key] = apply_patch(base_val, patch_val, delete)
            else:
                result[key] = copy.deepcopy(patch_val)
        else:
            result[key] = copy.deepcopy(base[key])
    for key in patch:
        if key not in base:
            patch_val = patch[key]
            if patch_val is delete:
                continue
            result[key] = copy.deepcopy(patch_val)
    return result
