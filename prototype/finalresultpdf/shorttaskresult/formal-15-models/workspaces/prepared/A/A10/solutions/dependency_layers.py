"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(f"Dependency cycle involving {self.nodes}")


def dependency_layers(edges):
    # Track first occurrence order
    nodes_order = []
    seen_nodes = set()
    # Adjacency list: node -> set of dependencies
    dependencies = {}
    reverse_deps = {}
    in_degree = {}
    
    # Process edges exactly once
    processed_edges = set()
    for node, dep in edges:
        # Track node first appearance
        if node not in seen_nodes:
            seen_nodes.add(node)
            nodes_order.append(node)
            dependencies[node] = set()
            reverse_deps[node] = set()
            in_degree[node] = 0
        if dep not in seen_nodes:
            seen_nodes.add(dep)
            nodes_order.append(dep)
            dependencies[dep] = set()
            reverse_deps[dep] = set()
            in_degree[dep] = 0
        
        # Deduplicate edges
        edge_key = (node, dep)
        if edge_key not in processed_edges:
            processed_edges.add(edge_key)
            dependencies[node].add(dep)
            reverse_deps[dep].add(node)
            in_degree[node] += 1
    
    # Kahn's algorithm for topological sort
    layers = []
    # Nodes with zero in-degree initially
    current_layer = [n for n in nodes_order if in_degree[n] == 0]
    
    while current_layer:
        layers.append(current_layer)
        next_in_degree = in_degree.copy()
        for n in current_layer:
            for dependent in reverse_deps[n]:
                next_in_degree[dependent] -= 1
        
        # Prepare next layer
        next_layer = []
        processed = set(n for layer in layers for n in layer)
        for n in nodes_order:
            if n not in processed and next_in_degree[n] == 0:
                next_layer.append(n)
        
        in_degree = next_in_degree
        current_layer = next_layer
    
    # Check for cycles
    total_processed = sum(len(layer) for layer in layers)
    if total_processed < len(nodes_order):
        # Collect remaining (cyclic/blocked) nodes
        remaining = []
        processed = set(n for layer in layers for n in layer)
        for n in nodes_order:
            if n not in processed:
                remaining.append(n)
        raise DependencyCycleError(remaining)
    
    return layers
