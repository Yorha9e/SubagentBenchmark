"""Implement the public contract from TASKS.md."""

import copy


class _DELETE:
    def __deepcopy__(self, memo):
        return self


DELETE = _DELETE()


def apply_patch(base, patch, delete=DELETE):
    if type(base) is not dict:
        raise TypeError("base must be a plain dict")
    if type(patch) is not dict:
        raise TypeError("patch must be a plain dict")

    def _merge(b, p):
        result = copy.deepcopy(b)
        for k, pv in p.items():
            if pv is delete:
                result.pop(k, None)
                continue
            old = result.get(k)
            if type(old) is dict and type(pv) is dict:
                result[k] = _merge(old, pv)
            else:
                result[k] = copy.deepcopy(pv)
        return result

    return _merge(base, patch)
