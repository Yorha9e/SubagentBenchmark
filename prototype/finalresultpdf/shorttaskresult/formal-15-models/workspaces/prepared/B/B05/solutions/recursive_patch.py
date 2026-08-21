import copy


class _DeleteType:
    def __deepcopy__(self, memo):
        return self

    def __copy__(self, memo):
        return self

    def __repr__(self):
        return "<DELETE>"


DELETE = _DeleteType()


def apply_patch(base, patch, delete=DELETE):
    if type(base) is not dict or type(patch) is not dict:
        raise TypeError("base and patch must be plain dict")

    result = copy.deepcopy(base)

    for key, patch_value in patch.items():
        if patch_value is delete:
            result.pop(key, None)
        elif key in result and type(result[key]) is dict and type(patch_value) is dict:
            result[key] = apply_patch(result[key], patch_value, delete=delete)
        else:
            result[key] = copy.deepcopy(patch_value)

    return result
