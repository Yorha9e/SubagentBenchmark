"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)


def dependency_layers(edges):
    # Collect nodes and edges, consuming the iterable exactly once.
    first_appearance = {}
    nodes = []
    adj = {}
    seen_edges = set()
    
    order = 0
    for node, dep in edges:
        for n in (node, dep):
            if n not in first_appearance:
                first_appearance[n] = order
                nodes.append(n)
                order += 1
            if n not in adj:
                adj[n] = set()
        if (node, dep) not in seen_edges:
            seen_edges.add((node, dep))
            adj[dep].add(node)
    
    # Compute in-degrees.
    in_degree = {n: 0 for n in nodes}
    for node in nodes:
        for dep in adj[node]:
            in_degree[dep] = in_degree.get(dep, 0) + 1
    
    # Kahn's algorithm, iterative.
    remaining = set(nodes)
    layers = []
    
    while True:
        # Find nodes with in-degree 0 in first-appearance order.
        ready = sorted(
            [n for n in remaining if in_degree.get(n, 0) == 0],
            key=lambda n: first_appearance[n],
        )
        if not ready:
            break
        
        layer = []
        for node in ready:
            remaining.remove(node)
            layer.append(node)
            for dep in adj[node]:
                if dep in remaining:
                    in_degree[dep] -= 1
        layers.append(layer)
    
    if remaining:
        cyclic = sorted(remaining, key=lambda n: first_appearance[n])
        raise DependencyCycleError(cyclic)
    
    return layers
