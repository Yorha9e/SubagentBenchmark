"""Implement the public contract from TASKS.md."""

DELETE = object()


def _deep_copy(obj):
    """Create a deep copy of a plain dict or return the value as-is."""
    if isinstance(obj, dict) and type(obj) is dict:
        return {k: _deep_copy(v) for k, v in obj.items()}
    return obj


def apply_patch(base, patch, delete=DELETE):
    # Validate inputs are plain dicts
    if type(base) is not dict:
        raise TypeError("base must be a plain dict")
    if type(patch) is not dict:
        raise TypeError("patch must be a plain dict")
    
    # Start with a deep copy of base to ensure detachment
    result = _deep_copy(base)
    
    # Process each key in patch order
    for key, patch_value in patch.items():
        # Handle deletion
        if patch_value is delete:
            if key in result:
                del result[key]
            continue
        
        # Check if both values are plain dicts for recursive merge
        if key in result and type(result[key]) is dict and type(patch_value) is dict:
            result[key] = apply_patch(result[key], patch_value, delete)
        else:
            # Replace with deep copy of patch value
            result[key] = _deep_copy(patch_value)
    
    return result
