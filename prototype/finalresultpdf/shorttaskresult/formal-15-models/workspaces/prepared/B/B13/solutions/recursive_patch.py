"""Implement the public contract from TASKS.md."""

import copy


class _DeleteSentinel:
    """Unique sentinel for deletion. Returns itself on deepcopy."""
    def __repr__(self):
        return "<DELETE>"

    def __deepcopy__(self, memo):
        return self

    def __copy__(self):
        return self


DELETE = _DeleteSentinel()


def apply_patch(base, patch, delete=DELETE):
    if type(base) is not dict:
        raise TypeError(f"base must be a dict, got {type(base).__name__}")
    if type(patch) is not dict:
        raise TypeError(f"patch must be a dict, got {type(patch).__name__}")

    result = copy.deepcopy(base)

    # Process patch items in their encounter order
    for key, patch_value in patch.items():
        if patch_value is delete:
            # Deletion: remove key if it exists
            result.pop(key, None)
        elif key in result:
            old_value = result[key]
            # Recursive merge only when both are plain dicts
            if type(old_value) is dict and type(patch_value) is dict:
                result[key] = apply_patch(old_value, patch_value, delete=delete)
            else:
                # Replace entire value with deep copy
                result[key] = copy.deepcopy(patch_value)
        else:
            # New key: deep copy and append at end
            result[key] = copy.deepcopy(patch_value)

    return result
