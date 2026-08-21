"""Implement the public contract from TASKS.md."""

DELETE = object()


def apply_patch(base, patch, delete=DELETE):
    def deep_copy(obj):
        if isinstance(obj, dict) and type(obj) is dict:
            return {k: deep_copy(v) for k, v in obj.items()}
        # We don't need to copy other mutable types since they are replaced completely
        return obj
    
    def merge(current, patch_dict):
        result = {}
        # Copy existing keys from current
        for key, value in current.items():
            if key not in patch_dict or patch_dict[key] is not delete:
                result[key] = deep_copy(value)
        
        # Apply patch keys
        for key, value in patch_dict.items():
            if value is delete:
                if key in result:
                    del result[key]
            else:
                if key in current and isinstance(current[key], dict) and type(current[key]) is dict and \
                   isinstance(value, dict) and type(value) is dict:
                    # Recursively merge
                    result[key] = merge(current[key], value)
                else:
                    # Replace entire value
                    result[key] = deep_copy(value)
        return result
    
    # Ensure inputs are plain dicts
    assert isinstance(base, dict) and type(base) is dict
    assert isinstance(patch, dict) and type(patch) is dict
    
    return merge(base, patch)
