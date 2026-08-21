"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__("dependency cycle: {!r}".format(self.nodes))


def dependency_layers(edges):
    order = []
    order_index = {}
    adjacency = {}
    indegree = {}
    seen_edges = set()

    def remember(node):
        if node not in order_index:
            order_index[node] = len(order)
            order.append(node)
            adjacency[node] = []
            indegree[node] = 0

    for node, dependency in edges:
        remember(node)
        remember(dependency)

        edge = (node, dependency)
        if edge in seen_edges:
            continue
        seen_edges.add(edge)
        adjacency[dependency].append(node)
        indegree[node] += 1

    ready = [node for node in order if indegree[node] == 0]
    layers = []
    processed = set()

    while ready:
        layer = ready
        layers.append(layer)
        next_ready = []

        for dependency in layer:
            processed.add(dependency)
            for node in adjacency[dependency]:
                indegree[node] -= 1
                if indegree[node] == 0:
                    next_ready.append(node)

        next_ready.sort(key=order_index.__getitem__)
        ready = next_ready

    if len(processed) != len(order):
        remaining = [node for node in order if node not in processed]
        raise DependencyCycleError(remaining)

    return layers
