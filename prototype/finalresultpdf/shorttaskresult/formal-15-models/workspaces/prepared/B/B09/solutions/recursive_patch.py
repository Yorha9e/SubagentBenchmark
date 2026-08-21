"""Implement the public contract from TASKS.md."""
import copy


class _DeleteSentinel:
    def __deepcopy__(self, memo):
        return self


DELETE = _DeleteSentinel()


def apply_patch(base, patch, delete=DELETE):
    if type(base) is not dict or type(patch) is not dict:
        raise TypeError("base and patch must be plain dict objects")
    
    result = copy.deepcopy(base)
    
    for key, patch_value in patch.items():
        if patch_value is delete:
            if key in result:
                del result[key]
        elif key in result and type(result[key]) is dict and type(patch_value) is dict:
            result[key] = apply_patch(result[key], patch_value, delete)
        else:
            result[key] = copy.deepcopy(patch_value)
    
    return result
