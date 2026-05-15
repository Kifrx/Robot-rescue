from core.graph_data import edges, nodes

# GET NEIGHBORS
def get_neighbors(node, blocked_nodes=None):
    if blocked_nodes is None:
        blocked_nodes = set()

    full_neighbors = edges.get(node, {})

    # Filter node yang tidak diblok
    return {
        n: w for n, w in full_neighbors.items()
        if n not in blocked_nodes
    }

# BFS
def run_bfs(start, goal, blocked_nodes=None):
    if blocked_nodes is None:
        blocked_nodes = set()

    queue = [[start]]
    visited = set()

    while queue:
        path = queue.pop(0)
        current = path[-1]

        if current == goal:
            return path

        if current not in visited:
            visited.add(current)

            for neighbor in get_neighbors(current, blocked_nodes):
                if neighbor not in visited:
                    new_path = path + [neighbor]
                    queue.append(new_path)

    return []

# DIJKSTRA
def run_dijkstra(start, goal, blocked_nodes=None):
    if blocked_nodes is None:
        blocked_nodes = set()

    distances = {node: float('inf') for node in nodes}
    parent = {}
    unvisited = set(nodes)

    distances[start] = 0

    while unvisited:
        # Ambil node dengan jarak minimum
        current = min(unvisited, key=lambda node: distances[node])

        if distances[current] == float('inf'):
            break

        if current == goal:
            break

        unvisited.remove(current)

        for neighbor, weight in get_neighbors(current, blocked_nodes).items():
            if neighbor in unvisited:
                new_distance = distances[current] + weight

                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parent[neighbor] = current

    # BACKTRACK
    path = []
    curr = goal

    if curr in parent or curr == start:
        while curr is not None:
            path.append(curr)
            curr = parent.get(curr)

    path.reverse()

    if path and path[0] == start:
        return path

    return []
