from core.graph_data import edges, nodes

def get_neighbors(node):
    return edges.get(node, {})

def run_bfs(start, goal):
    queue = []
    queue.append([start]) 
    
    visited = [] 
    
    while len(queue) > 0:
        path = queue.pop(0) 
        current = path[-1]
        
        if current == goal:
            return path
            
        if current not in visited:
            visited.append(current)
            
            # Looping tetangga
            for neighbor in get_neighbors(current):
                if neighbor not in visited:
                    # Bikin list rute baru
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
                    
    return []

def run_dijkstra(start, goal):
    
    distances = {}
    parent = {}
    unvisited = []
    
    # Inisialisasi semua node dengan jarak 
    for node in nodes:
        distances[node] = float('inf')
        unvisited.append(node)
        
    distances[start] = 0
    
    while len(unvisited) > 0:
        # Cari node dengan jarak terpendek 
        min_dist = float('inf')
        current = None
        
        for node in unvisited:
            if distances[node] < min_dist:
                min_dist = distances[node]
                current = node
                
        #  stop jika smpai tujuan
        if current is None or current == goal:
            break
            
        unvisited.remove(current)
        
        # Cek dan update jarak tetangga
        for neighbor, weight in get_neighbors(current).items():
            if neighbor in unvisited:
                new_distance = distances[current] + weight
                
                #  update jarak 
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    parent[neighbor] = current
                    
    # Backtracking
    path = []
    curr = goal
    

    if curr in parent or curr == start:
        while curr is not None:
            path.append(curr)
            curr = parent.get(curr) 
            
    path.reverse() #
    
    if len(path) > 0 and path[0] == start:
        return path
        
    return []