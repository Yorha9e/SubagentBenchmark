"""Recursive dict patching with DELETE sentinel."""

import copy


class _DeleteSentinel:
    """Unique sentinel for marking keys to delete."""

    def __repr__(self):
        return "DELETE"

    def __deepcopy__(self, memo):
        # Always return the same singleton to avoid creating copies
        return self


DELETE = _DeleteSentinel()


def apply_patch(base, patch, delete=DELETE):
    """Recursively merge *patch* into *base* and return a detached copy.

    Rules:
    - Only plain ``dict`` instances are merged recursively; everything else is
      replaced wholesale with a deep copy of the patch value.
    - A patch value that *is* ``delete`` (by identity) removes the
      corresponding key.
    - Key order: retained base keys keep their positions; genuinely new keys
      appear at the end in patch encounter order.  This applies recursively and
      across replacement boundaries (a replaced dict adopts patch order).
    - Neither input is mutated; the result shares no mutable container with
      either input.
    """
    if type(base) is not dict or type(patch) is not dict:
        raise TypeError("base and patch must be plain dict")

    return _merge(copy.deepcopy(base), patch, delete)


def _merge(base_copy, patch, delete):
    """Apply *patch* onto an already-deep-copied *base_copy*."""

    for key, pval in patch.items():
        if pval is delete:
            # Deletion by identity
            base_copy.pop(key, None)
            continue

        if key in base_copy:
            old_val = base_copy[key]
            if type(old_val) is dict and type(pval) is dict:
                # Both plain dicts → recursive merge (order preserved from base)
                base_copy[key] = _merge(old_val, pval, delete)
            else:
                # Replace: need to keep key's position, so assign in-place.
                # Deep-copy the patch value to detach from patch input.
                base_copy[key] = copy.deepcopy(pval)
        else:
            # New key – append at end with deep-copied value
            base_copy[key] = copy.deepcopy(pval)

    return base_copy
