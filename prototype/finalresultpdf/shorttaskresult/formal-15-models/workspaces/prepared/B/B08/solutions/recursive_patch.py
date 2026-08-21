"""Implement the public contract from TASKS.md."""
import copy


class _DeleteSentinel:
    _instance = None

    def __deepcopy__(self, memo):
        return self

    def __repr__(self):
        return "DELETE"


DELETE = _DeleteSentinel()


def apply_patch(base, patch, delete=DELETE):
    if type(base) is not dict:
        raise TypeError("base must be a plain dict")
    if type(patch) is not dict:
        raise TypeError("patch must be a plain dict")

    result = copy.deepcopy(base)
    _merge_into(result, patch, delete)
    return result


def _merge_into(target, patch, delete):
    for key, patch_value in patch.items():
        if patch_value is delete:
            if key in target:
                del target[key]
            continue

        if key in target and type(target[key]) is dict and type(patch_value) is dict:
            _merge_into(target[key], patch_value, delete)
        else:
            target[key] = copy.deepcopy(patch_value)
