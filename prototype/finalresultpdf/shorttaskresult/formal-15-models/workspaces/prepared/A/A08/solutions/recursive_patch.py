"""Implement the public contract from TASKS.md."""
import copy

DELETE = object()


def _is_plain_dict(x):
    return type(x) is dict


def apply_patch(base, patch, delete=DELETE):
    result = {}

    # Retained base keys keep their positions
    for key, value in base.items():
        if key in patch:
            patch_val = patch[key]
            if patch_val is delete:
                # Deletion: skip this key
                continue
            elif _is_plain_dict(value) and _is_plain_dict(patch_val):
                # Recursively merge plain dicts
                result[key] = apply_patch(value, patch_val, delete)
            else:
                # Replace with detached copy
                result[key] = copy.deepcopy(patch_val)
        else:
            # Keep base value, detached
            result[key] = copy.deepcopy(value)

    # Genuinely new keys follow patch encounter order
    for key, value in patch.items():
        if key not in base:
            if value is delete:
                # Deleting a non-existent key: nothing to do
                continue
            result[key] = copy.deepcopy(value)

    return result
