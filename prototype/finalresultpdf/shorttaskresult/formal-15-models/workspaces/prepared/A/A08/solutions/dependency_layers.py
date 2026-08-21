"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(f"Dependency cycle: {self.nodes}")


def dependency_layers(edges):
    # Track first-appearance order and build graph
    first_appearance = []
    seen = set()
    dependents = {}   # dep -> list of nodes that depend on it
    dependencies = {} # node -> set of its dependencies

    def add_node(node):
        if node not in seen:
            seen.add(node)
            first_appearance.append(node)
            dependents[node] = []
            dependencies[node] = set()

    # Consume edges exactly once
    for node, dep in edges:
        add_node(node)
        add_node(dep)
        # Deduplicate repeated edges
        if dep not in dependencies[node]:
            dependencies[node].add(dep)
            dependents[dep].append(node)

    order_index = {node: i for i, node in enumerate(first_appearance)}

    # In-degree count for each node
    in_degree = {node: len(dependencies[node]) for node in first_appearance}

    # Kahn's algorithm, layer by layer (iterative, no recursion)
    layers = []
    current_layer = [node for node in first_appearance if in_degree[node] == 0]

    while current_layer:
        layers.append(current_layer)
        next_layer_set = set()
        for node in current_layer:
            for dependent in dependents[node]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    next_layer_set.add(dependent)
        # Maintain first-appearance order within each layer
        current_layer = sorted(next_layer_set, key=lambda n: order_index[n])

    # Check for cycles
    resolved_count = sum(len(layer) for layer in layers)
    if resolved_count < len(first_appearance):
        remaining = [node for node in first_appearance if in_degree[node] > 0]
        raise DependencyCycleError(remaining)

    return layers
