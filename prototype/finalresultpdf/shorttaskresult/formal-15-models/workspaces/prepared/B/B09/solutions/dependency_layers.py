"""Implement the public contract from TASKS.md."""


class DependencyCycleError(ValueError):
    def __init__(self, nodes):
        self.nodes = tuple(nodes)
        super().__init__(f"Dependency cycle involving nodes: {self.nodes}")


def dependency_layers(edges):
    nodes = []
    node_to_id = {}
    hash_buckets = {}
    
    indegree = []
    dependents = []
    seen_edges = set()
    
    def get_id(node):
        try:
            node_hash = hash(node)
            if node_hash in hash_buckets:
                for existing_id in hash_buckets[node_hash]:
                    if nodes[existing_id] == node:
                        return existing_id
            bucket = hash_buckets.setdefault(node_hash, [])
        except TypeError:
            for existing_id, existing_node in enumerate(nodes):
                if existing_node == node:
                    return existing_id
            bucket = None
        
        node_id = len(nodes)
        nodes.append(node)
        indegree.append(0)
        dependents.append([])
        if bucket is not None:
            bucket.append(node_id)
        return node_id
    
    for node, dependency in edges:
        node_id = get_id(node)
        dep_id = get_id(dependency)
        
        edge_pair = (node_id, dep_id)
        if edge_pair not in seen_edges:
            seen_edges.add(edge_pair)
            indegree[node_id] += 1
            dependents[dep_id].append(node_id)
    
    result = []
    current_layer = [i for i in range(len(nodes)) if indegree[i] == 0]
    processed = 0
    
    while current_layer:
        current_layer.sort()
        result.append([nodes[i] for i in current_layer])
        processed += len(current_layer)
        
        next_layer = []
        for dep_id in current_layer:
            for node_id in dependents[dep_id]:
                indegree[node_id] -= 1
                if indegree[node_id] == 0:
                    next_layer.append(node_id)
        current_layer = next_layer
    
    if processed < len(nodes):
        remaining = [i for i in range(len(nodes)) if indegree[i] > 0]
        remaining.sort()
        raise DependencyCycleError([nodes[i] for i in remaining])
    
    return result
