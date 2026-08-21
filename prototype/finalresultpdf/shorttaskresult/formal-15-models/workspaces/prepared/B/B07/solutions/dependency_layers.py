"""Layer nodes by their dependencies."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(f"dependency cycle or blocked nodes: {self.nodes!r}")


def _nodes_equal(left, right):
    if left is right:
        return True
    try:
        result = left == right
    except Exception:
        return False
    try:
        return bool(result)
    except Exception:
        return False


def dependency_layers(edges):
    """Return dependency-first topological layers for a one-shot edge stream."""
    nodes = []
    indegree = []
    dependents = []
    hash_buckets = {}
    unhashable_ids = []

    def find_node(value):
        try:
            value_hash = hash(value)
        except TypeError:
            for index, existing in enumerate(nodes):
                if _nodes_equal(existing, value):
                    return index
            return None

        for index in hash_buckets.get(value_hash, ()):
            if _nodes_equal(nodes[index], value):
                return index

        for index in unhashable_ids:
            if _nodes_equal(nodes[index], value):
                return index
        return None

    def intern(value):
        index = find_node(value)
        if index is not None:
            return index

        index = len(nodes)
        nodes.append(value)
        indegree.append(0)
        dependents.append([])
        try:
            value_hash = hash(value)
        except TypeError:
            unhashable_ids.append(index)
        else:
            hash_buckets.setdefault(value_hash, []).append(index)
        return index

    seen_edges = set()
    for node, dependency in edges:
        node_id = intern(node)
        dependency_id = intern(dependency)
        edge = (node_id, dependency_id)
        if edge in seen_edges:
            continue
        seen_edges.add(edge)
        indegree[node_id] += 1
        dependents[dependency_id].append(node_id)

    ready = [index for index, degree in enumerate(indegree) if degree == 0]
    layers = []
    processed = 0

    while ready:
        ready.sort()
        layers.append([nodes[index] for index in ready])
        processed += len(ready)
        next_ready = []
        for dependency_id in ready:
            for node_id in dependents[dependency_id]:
                indegree[node_id] -= 1
                if indegree[node_id] == 0:
                    next_ready.append(node_id)
        ready = next_ready

    if processed != len(nodes):
        remaining = tuple(
            nodes[index]
            for index, degree in enumerate(indegree)
            if degree > 0
        )
        raise DependencyCycleError(remaining)

    return layers
