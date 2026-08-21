"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    """Raised when edges contain a directed cycle."""

    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(f"dependency cycle detected: {', '.join(map(repr, nodes))}")


def dependency_layers(edges):
    """Return topological layers from *edges*, each an iterable of ``(node, dependency)``.

    Dependencies appear in earlier layers than their dependents.  *edges* is
    consumed exactly once.
    """
    all_nodes = []  # actual objects indexed by ID
    hash_map = {}   # hashable value => ID (fast path)

    indegree = []     # indegree[id] — count of dependencies for this node
    dependents = []   # dependents[dep_id] = list of dependent node IDs
    seen_edges = set()  # (node_id, dep_id) pairs

    def _register(value):
        """Return existing ID for *value* or create a new one."""
        # Fast path: hashable values
        try:
            hash(value)
            if value in hash_map:
                return hash_map[value]
        except TypeError:
            pass

        # Fall back to linear equality scan (covers unhashable and hash-collision
        # cases where an equal hashable node was already stored)
        for i, existing in enumerate(all_nodes):
            if existing == value:
                return i

        idx = len(all_nodes)
        all_nodes.append(value)
        indegree.append(0)
        dependents.append([])
        try:
            hash(value)
            hash_map[value] = idx
        except TypeError:
            pass
        return idx

    # ---------- single pass over the edge stream ----------
    for node, dependency in edges:
        node_id = _register(node)
        dep_id = _register(dependency)

        edge_key = (node_id, dep_id)
        if edge_key in seen_edges:
            continue
        seen_edges.add(edge_key)

        indegree[node_id] += 1
        dependents[dep_id].append(node_id)

    if not all_nodes:
        return []

    # ---------- Kahn's algorithm (non-recursive) ----------
    queue = [i for i in range(len(all_nodes)) if indegree[i] == 0]
    result = []
    processed = 0

    while queue:
        queue.sort()  # deterministic order by first-appearance ID
        layer = [all_nodes[i] for i in queue]
        result.append(layer)

        next_queue = []
        for node_id in queue:
            processed += 1
            for dependent_id in dependents[node_id]:
                indegree[dependent_id] -= 1
                if indegree[dependent_id] == 0:
                    next_queue.append(dependent_id)
        queue = next_queue

    if processed < len(all_nodes):
        cyclic = [all_nodes[i] for i in range(len(all_nodes)) if indegree[i] > 0]
        raise DependencyCycleError(cyclic)

    return result
