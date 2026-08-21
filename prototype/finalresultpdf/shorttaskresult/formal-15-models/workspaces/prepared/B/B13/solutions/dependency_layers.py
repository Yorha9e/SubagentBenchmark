"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    """Raised when a dependency cycle is detected."""

    def __init__(self, nodes, message=None):
        self.nodes = tuple(nodes)
        if message is None:
            message = f"dependency cycle involving {self.nodes}"
        super().__init__(message)


def dependency_layers(edges):
    """Compute dependency layers from an iterable of (node, dependency) pairs.

    Returns a list of lists, with dependencies in earlier layers.
    """
    # Consume exactly once, track first appearance order
    first_appearance = []  # list of (id, actual_object)
    id_map = {}  # maps actual object (or None for unhashable) -> id
    node_objects = {}  # id -> actual object

    # Build graph structures
    next_id = [0]

    def get_or_create_id(obj):
        """Get or create an integer ID for an object, handling unhashable types."""
        # Try hash-based fast path
        try:
            key = (type(obj), obj)
            if key in id_map:
                return id_map[key]
        except TypeError:
            key = None

        # For hashable: use hash bucket
        if key is not None:
            id_map[key] = next_id[0]
            node_objects[next_id[0]] = obj
            first_appearance.append(next_id[0])
            next_id[0] += 1
            return next_id[0] - 1

        # For unhashable: linear scan by equality
        for existing_id, existing_obj in zip(
            range(len(first_appearance)),
            [node_objects[i] for i in first_appearance]
        ):
            if type(existing_obj) is type(obj) and existing_obj == obj:
                return existing_id
        # New unhashable node
        node_id = next_id[0]
        node_objects[node_id] = obj
        first_appearance.append(node_id)
        next_id[0] += 1
        return node_id

    indegree = {}  # id -> int
    dependents = {}  # id -> list of ids that depend on this
    seen_edges = set()

    for item in edges:
        node_obj, dep_obj = item
        node_id = get_or_create_id(node_obj)
        dep_id = get_or_create_id(dep_obj)

        edge = (node_id, dep_id)
        if edge in seen_edges:
            continue
        seen_edges.add(edge)

        if node_id not in indegree:
            indegree[node_id] = 0
        if dep_id not in indegree:
            indegree[dep_id] = 0

        indegree[node_id] += 1
        dependents.setdefault(dep_id, []).append(node_id)

    # Kahn's algorithm (iterative, layer-by-layer)
    # Initial layer: all nodes with indegree 0, sorted by first appearance
    zero_indegree = sorted([nid for nid in indegree if indegree[nid] == 0])
    layers = []
    processed = set()

    current_layer = zero_indegree
    while current_layer:
        layers.append([node_objects[nid] for nid in current_layer])
        processed.update(current_layer)

        next_layer = []
        for nid in current_layer:
            for dep_id in dependents.get(nid, []):
                indegree[dep_id] -= 1
                if indegree[dep_id] == 0 and dep_id not in processed:
                    next_layer.append(dep_id)

        # Sort by first appearance order (which is the id order)
        next_layer.sort()
        current_layer = next_layer

    # If there are remaining nodes, they form cycles (or are blocked by cycles)
    remaining = sorted([nid for nid in indegree if nid not in processed])
    if remaining:
        raise DependencyCycleError([node_objects[nid] for nid in remaining])

    return layers
