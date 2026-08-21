"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes, message=None):
        self.nodes = tuple(nodes)
        if message is None:
            message = f"dependency cycle among {list(self.nodes)}"
        super().__init__(message)


def dependency_layers(edges):
    # First pass: consume the iterable exactly once and record first appearance.
    node_ids = {}
    nodes = []
    # Use a list of (node_id, dependency_id) for deduplicated edges.
    seen_edges = set()
    edge_list = []

    def _get_id(obj):
        # Fast path for hashable objects using a dict mapping value -> id.
        try:
            return node_ids[obj]
        except TypeError:
            # Unhashable: fall back to equality search.
            for idx, existing in enumerate(nodes):
                if existing == obj:
                    return idx
            new_id = len(nodes)
            nodes.append(obj)
            return new_id
        except KeyError:
            new_id = len(nodes)
            node_ids[obj] = new_id
            nodes.append(obj)
            return new_id

    for node, dependency in edges:
        node_id = _get_id(node)
        dependency_id = _get_id(dependency)
        edge_key = (node_id, dependency_id)
        if edge_key not in seen_edges:
            seen_edges.add(edge_key)
            edge_list.append(edge_key)

    node_count = len(nodes)
    if node_count == 0:
        return []

    indegree = [0] * node_count
    dependents = [[] for _ in range(node_count)]

    for node_id, dependency_id in edge_list:
        indegree[node_id] += 1
        dependents[dependency_id].append(node_id)

    # Kahn's algorithm, layer by layer.
    current = [idx for idx in range(node_count) if indegree[idx] == 0]
    processed = 0
    layers = []

    while current:
        layers.append([nodes[idx] for idx in current])
        processed += len(current)
        next_layer = []
        for dependency_id in current:
            for dependent_id in dependents[dependency_id]:
                indegree[dependent_id] -= 1
                if indegree[dependent_id] == 0:
                    next_layer.append(dependent_id)
        current = next_layer

    if processed < node_count:
        remaining = [idx for idx in range(node_count) if indegree[idx] > 0]
        raise DependencyCycleError([nodes[idx] for idx in remaining])

    return layers
