"""Implement the public contract from TASKS.md."""

DELETE = object()


def apply_patch(base, patch, delete=DELETE):
    if type(base) is not dict or type(patch) is not dict:
        raise TypeError("base and patch must be plain dicts")

    def _clone(d):
        out = {}
        for k, v in d.items():
            out[k] = _clone(v) if type(v) is dict else v
        return out

    result = _clone(base)

    for key, pval in patch.items():
        if pval is delete:
            result.pop(key, None)
        elif key in result and type(result[key]) is dict and type(pval) is dict:
            result[key] = apply_patch(result[key], pval, delete)
        else:
            result[key] = _clone(pval) if type(pval) is dict else pval

    return result
