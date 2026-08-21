"""Implement the public contract from TASKS.md."""

import copy


DELETE = object()


def _is_plain_dict(value):
    return type(value) is dict


def apply_patch(base, patch, delete=DELETE):
    if not _is_plain_dict(base) or not _is_plain_dict(patch):
        raise TypeError("base and patch must be plain dicts")

    memo = {}
    merged = {}

    def detached(value):
        return copy.deepcopy(value, memo)

    def merge(old, update):
        pair = (id(old), id(update))
        existing = merged.get(pair)
        if existing is not None:
            return existing

        result = {}
        merged[pair] = result

        for key, old_value in old.items():
            if key in update:
                new_value = update[key]
                if new_value is delete:
                    continue
                if _is_plain_dict(old_value) and _is_plain_dict(new_value):
                    result[key] = merge(old_value, new_value)
                else:
                    result[key] = detached(new_value)
            else:
                result[key] = detached(old_value)

        for key, new_value in update.items():
            if key in old or new_value is delete:
                continue
            result[key] = detached(new_value)

        return result

    return merge(base, patch)
