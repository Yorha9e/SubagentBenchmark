"""Implement the public contract from TASKS.md."""
import copy


class _DeleteSentinel:
    __slots__ = ()

    def __deepcopy__(self, memo):
        return self


DELETE = _DeleteSentinel()


def apply_patch(base, patch, delete=DELETE):
    # Validate inputs are plain dicts
    if type(base) is not dict or type(patch) is not dict:
        raise TypeError("base and patch must be plain dict objects")
    
    # Deepcopy base to create a detached result
    result = copy.deepcopy(base)
    
    # Process patch items in order
    for key, patch_value in patch.items():
        if patch_value is delete:
            # Delete the key if it exists
            if key in result:
                del result[key]
        else:
            # Check if both current value and patch value are plain dicts
            if key in result and type(result[key]) is dict and type(patch_value) is dict:
                # Recursively merge
                result[key] = apply_patch(result[key], patch_value, delete=delete)
            else:
                # Replace entirely with deep copy of patch value
                result[key] = copy.deepcopy(patch_value)
    
    return result
