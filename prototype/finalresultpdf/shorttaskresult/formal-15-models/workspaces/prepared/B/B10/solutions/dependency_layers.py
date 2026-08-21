"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(f"Cycle detected in nodes: {self.nodes}")


def dependency_layers(edges):
    nodes = []  # list of first-encountered node objects, index = id
    node_to_id = {}  # hashable nodes map here
    node_id_to_index = []  # for unhashable nodes, list of (node, id)
    next_id = 0

    indegree = {}
    dependents = {}
    seen_edges = set()

    # Consume edges exactly once
    for node, dependency in edges:
        # Process node first
        node_id = None
        # Try hashable path first
        try:
            if node in node_to_id:
                node_id = node_to_id[node]
        except TypeError:
            # Unhashable, check via equality
            for stored_node, stored_id in node_id_to_index:
                if stored_node == node:
                    node_id = stored_id
                    break
        # If not found, add new node
        if node_id is None:
            node_id = next_id
            next_id += 1
            nodes.append(node)
            # Update index structures
            try:
                node_to_id[node] = node_id
            except TypeError:
                node_id_to_index.append((node, node_id))
            # Initialize indegree and dependents
            indegree[node_id] = 0
            dependents[node_id] = []

        # Process dependency
        dep_id = None
        try:
            if dependency in node_to_id:
                dep_id = node_to_id[dependency]
        except TypeError:
            for stored_node, stored_id in node_id_to_index:
                if stored_node == dependency:
                    dep_id = stored_id
                    break
        if dep_id is None:
            dep_id = next_id
            next_id += 1
            nodes.append(dependency)
            try:
                node_to_id[dependency] = dep_id
            except TypeError:
                node_id_to_index.append((dependency, dep_id))
            indegree[dep_id] = 0
            dependents[dep_id] = []

        # Deduplicate edge
        edge = (node_id, dep_id)
        if edge not in seen_edges:
            seen_edges.add(edge)
            indegree[node_id] += 1
            dependents[dep_id].append(node_id)

    # Kahn's algorithm, non-recursive
    layers = []
    processed = 0
    total_nodes = len(nodes)

    while True:
        # Collect current layer (indegree == 0, ordered by id)
        current_layer_ids = [
            node_id for node_id in range(total_nodes)
            if indegree.get(node_id, 0) == 0
        ]
        if not current_layer_ids:
            break

        # Convert to node objects and add to layers
        layers.append([nodes[node_id] for node_id in current_layer_ids])
        processed += len(current_layer_ids)

        # Process dependents
        for node_id in current_layer_ids:
            for dependent_id in dependents[node_id]:
                indegree[dependent_id] -= 1
            # Mark as processed
            indegree[node_id] = -1

    # Check for cycles
    if processed < total_nodes:
        remaining_nodes = [
            nodes[node_id] for node_id in range(total_nodes)
            if indegree.get(node_id, 0) > 0
        ]
        raise DependencyCycleError(remaining_nodes)

    return layers
