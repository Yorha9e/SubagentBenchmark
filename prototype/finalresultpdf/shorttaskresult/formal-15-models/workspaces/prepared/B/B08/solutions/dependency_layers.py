"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(f"Dependency cycle involving {self.nodes}")


def dependency_layers(edges):
    # Map each unique node to an integer id based on first appearance.
    # We need to handle both hashable and unhashable nodes.
    nodes = []  # list of node objects by id
    hashable_map = {}  # hashable node -> id
    unhashable_list = []  # list of (node, id) for unhashable nodes

    def _get_id(node):
        # Try hashable path first
        try:
            if node in hashable_map:
                return hashable_map[node]
            # Check if it's really hashable by trying
            hash(node)
            new_id = len(nodes)
            nodes.append(node)
            hashable_map[node] = new_id
            return new_id
        except TypeError:
            # Unhashable: linear scan
            for existing_node, existing_id in unhashable_list:
                if existing_node == node:
                    return existing_id
            new_id = len(nodes)
            nodes.append(node)
            unhashable_list.append((node, new_id))
            return new_id

    indegree = {}  # id -> count of unique dependencies
    dependents = {}  # dependency_id -> list of dependent ids
    seen_edges = set()  # set of (dependent_id, dependency_id) tuples

    for node, dependency in edges:
        node_id = _get_id(node)
        dep_id = _get_id(dependency)

        if node_id not in indegree:
            indegree[node_id] = 0
        if dep_id not in indegree:
            indegree[dep_id] = 0
        if node_id not in dependents:
            dependents[node_id] = []
        if dep_id not in dependents:
            dependents[dep_id] = []

        edge_pair = (node_id, dep_id)
        if edge_pair not in seen_edges:
            seen_edges.add(edge_pair)
            indegree[node_id] += 1
            dependents[dep_id].append(node_id)

    total_nodes = len(nodes)

    # Kahn's algorithm, layer by layer
    layers = []
    current_layer = sorted([nid for nid in range(total_nodes) if indegree[nid] == 0])
    processed = 0

    while current_layer:
        layers.append([nodes[nid] for nid in current_layer])
        processed += len(current_layer)

        next_layer = []
        for dep_id in current_layer:
            for node_id in dependents.get(dep_id, []):
                indegree[node_id] -= 1
                if indegree[node_id] == 0:
                    next_layer.append(node_id)

        current_layer = sorted(next_layer)

    if processed < total_nodes:
        # Remaining nodes with indegree > 0 are in or blocked by a cycle
        remaining = sorted([nid for nid in range(total_nodes) if indegree[nid] > 0])
        raise DependencyCycleError([nodes[nid] for nid in remaining])

    return layers
