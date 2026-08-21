"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes=()):
        self.nodes = tuple(nodes)
        super().__init__(f"dependency cycle detected among {self.nodes!r}")


def dependency_layers(edges):
    nodes = []            # node id -> first-seen node object
    hash_index = {}       # hashable node -> id
    unhashable_index = [] # (node, id) pairs for unhashable nodes
    indegree = []         # deduplicated dependency count per node id
    dependents = []       # id -> list of ids that depend on it
    seen_edges = set()

    def register(node):
        node_id = len(nodes)
        nodes.append(node)
        indegree.append(0)
        dependents.append([])
        return node_id

    def intern(node):
        try:
            existing = hash_index.get(node)
        except TypeError:
            existing = None
            for other, other_id in unhashable_index:
                if node == other:
                    return other_id
            # Cross-path equality check against hashable nodes.
            for other, other_id in hash_index.items():
                if node == other:
                    return other_id
            node_id = register(node)
            unhashable_index.append((node, node_id))
            return node_id
        if existing is not None:
            return existing
        for other, other_id in unhashable_index:
            if node == other:
                return other_id
        node_id = register(node)
        hash_index[node] = node_id
        return node_id

    # Consume the one-shot iterable exactly once.
    for node, dependency in edges:
        node_id = intern(node)
        dep_id = intern(dependency)
        edge = (node_id, dep_id)
        if edge in seen_edges:
            continue
        seen_edges.add(edge)
        indegree[node_id] += 1
        dependents[dep_id].append(node_id)

    layers = []
    current = [node_id for node_id in range(len(nodes)) if indegree[node_id] == 0]
    processed = 0
    while current:
        current.sort()  # order by first appearance, not adjacency accident
        layers.append([nodes[node_id] for node_id in current])
        processed += len(current)
        next_layer = []
        for node_id in current:
            for dependent in dependents[node_id]:
                indegree[dependent] -= 1
                if indegree[dependent] == 0:
                    next_layer.append(dependent)
        current = next_layer

    if processed < len(nodes):
        remaining = tuple(
            nodes[node_id] for node_id in range(len(nodes)) if indegree[node_id] > 0
        )
        raise DependencyCycleError(remaining)
    return layers
