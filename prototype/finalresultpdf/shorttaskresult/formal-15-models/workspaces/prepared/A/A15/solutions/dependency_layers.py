"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(f"dependency cycle involving {self.nodes!r}")


def dependency_layers(edges):
    first_appearance = {}
    appearance_order = []
    seen_edges = set()
    dependencies = {}
    dependents = {}

    for node, dep in edges:
        for n in (node, dep):
            if n not in first_appearance:
                first_appearance[n] = len(appearance_order)
                appearance_order.append(n)

        if (node, dep) in seen_edges:
            continue
        seen_edges.add((node, dep))

        dependencies.setdefault(node, set()).add(dep)
        dependencies.setdefault(dep, set())
        dependents.setdefault(dep, set()).add(node)
        dependents.setdefault(node, set())

    in_degree = {node: len(dependencies[node]) for node in appearance_order}

    layers = []
    processed = set()

    while len(processed) < len(appearance_order):
        current_layer = [
            node
            for node in appearance_order
            if node not in processed and in_degree[node] == 0
        ]

        if not current_layer:
            remaining = [n for n in appearance_order if n not in processed]
            raise DependencyCycleError(remaining)

        layers.append(current_layer)
        for node in current_layer:
            processed.add(node)
            for dependent in dependents[node]:
                in_degree[dependent] -= 1

    return layers
