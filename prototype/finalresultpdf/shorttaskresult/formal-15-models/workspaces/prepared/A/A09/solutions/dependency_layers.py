"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(f"Dependency cycle involving nodes: {nodes}")


def dependency_layers(edges):
    # Track node appearance order
    node_order = []
    seen = set()
    
    # Build adjacency and reverse adjacency lists
    adj = {}  # node -> set of dependencies (what this node depends on)
    rev_adj = {}  # dependency -> set of nodes that depend on it
    
    # Process edges exactly once
    for node, dep in edges:
        # Track first appearance of both nodes
        for n in (node, dep):
            if n not in seen:
                seen.add(n)
                node_order.append(n)
                adj[n] = set()
                rev_adj[n] = set()
        
        # Deduplicate edges
        if dep not in adj[node]:
            adj[node].add(dep)
            rev_adj[dep].add(node)
    
    # Kahn's algorithm for topological sort
    # Calculate in-degrees (number of unmet dependencies)
    in_degree = {node: len(deps) for node, deps in adj.items()}
    
    # Find nodes with no dependencies
    result = []
    current_layer = []
    
    # Use a queue for Kahn's algorithm
    queue = []
    for node in node_order:
        if in_degree[node] == 0:
            queue.append(node)
    
    while queue:
        # Process all nodes in current layer
        layer_size = len(queue)
        current_layer = []
        
        # Process nodes in first-appearance order within this batch
        # Actually, we need to sort the queue by first-appearance to maintain stable order
        queue.sort(key=lambda n: node_order.index(n))
        
        for _ in range(layer_size):
            node = queue.pop(0)
            current_layer.append(node)
            
            # Update in-degree for nodes that depend on this one
            for dependent in rev_adj[node]:
                in_degree[dependent] -= 1
                if in_degree[dependent] == 0:
                    queue.append(dependent)
        
        result.append(current_layer)
    
    # Check for cycles (nodes with in_degree > 0 are in a cycle)
    cyclic_nodes = [node for node in node_order if in_degree[node] > 0]
    if cyclic_nodes:
        raise DependencyCycleError(cyclic_nodes)
    
    return result
