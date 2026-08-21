"""Recursive deep-merge patch with deletion sentinel."""

DELETE = object()


def _deep_copy(v):
    """Return a detached copy of *v* so the result never aliases an input."""
    if isinstance(v, dict):
        return {k: _deep_copy(val) for k, val in v.items()}
    if isinstance(v, list):
        return [_deep_copy(item) for item in v]
    if isinstance(v, tuple):
        return tuple(_deep_copy(item) for item in v)
    if isinstance(v, set):
        return {_deep_copy(item) for item in v}
    if isinstance(v, frozenset):
        return frozenset(_deep_copy(item) for item in v)
    if isinstance(v, bytearray):
        return bytearray(v)
    return v  # immutable scalars, bytes, str, etc.


def apply_patch(base, patch, delete=DELETE):
    """Recursively merge *patch* into *base* and return a detached result.

    - Values equal-by-identity to *delete* remove the key.
    - Recursive merge happens only when **both** sides are plain ``dict``
      objects (``type(x) is dict``).  Otherwise the patch value replaces.
    - Retained base keys keep their position; genuinely new keys follow
      patch encounter order (including inside nested merges).
    """
    result = {}

    # Keys from base — preserve their positional order.
    for key in base:
        if key in patch:
            pv = patch[key]
            if pv is delete:
                continue  # deletion: skip key entirely
            bv = base[key]
            if type(bv) is dict and type(pv) is dict:
                # Recursive merge — already produces a detached sub-result.
                result[key] = apply_patch(bv, pv, delete)
            else:
                # Replacement — deep-copy to avoid aliasing.
                result[key] = _deep_copy(pv)
        else:
            # Key untouched by patch — deep-copy to detach.
            result[key] = _deep_copy(base[key])

    # Genuinely new keys from patch, in encounter order.
    for key in patch:
        if key not in base:
            pv = patch[key]
            if pv is delete:
                continue
            result[key] = _deep_copy(pv)

    return result
