"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        node_repr = ", ".join(repr(node) for node in self.nodes)
        super().__init__(f"Dependency cycle involving: {node_repr}")


def dependency_layers(edges):
    nodes = []
    indegree = []
    dependents = []
    seen_edges = set()

    def get_id(obj):
        for index, existing in enumerate(nodes):
            if existing == obj:
                return index
        index = len(nodes)
        nodes.append(obj)
        indegree.append(0)
        dependents.append([])
        return index

    for node, dependency in edges:
        node_id = get_id(node)
        dependency_id = get_id(dependency)
        edge = (node_id, dependency_id)
        if edge in seen_edges:
            continue
        seen_edges.add(edge)
        indegree[node_id] += 1
        dependents[dependency_id].append(node_id)

    layers = []
    current_layer = [index for index, degree in enumerate(indegree) if degree == 0]
    current_layer.sort()
    processed = 0

    while current_layer:
        layers.append([nodes[index] for index in current_layer])
        processed += len(current_layer)

        next_layer = []
        for node_id in current_layer:
            for dependent_id in dependents[node_id]:
                indegree[dependent_id] -= 1
                if indegree[dependent_id] == 0:
                    next_layer.append(dependent_id)

        next_layer.sort()
        current_layer = next_layer

    if processed < len(nodes):
        blocked = [nodes[index] for index in range(len(nodes)) if indegree[index] > 0]
        raise DependencyCycleError(blocked)

    return layers
