from collections import deque
import heapq
from core.graph_data import edges

def get_neighbors(node):
    return edges.get(node, {})

def run_bfs(start, goal):
    queue = deque([(start, [start])])
    seen = {start}
    
    while queue:
        current, path = queue.popleft()
        if current == goal:
            return path
            
        for neighbor in get_neighbors(current):
            if neighbor not in seen:
                seen.add(neighbor)
                # path lama + node baru
                queue.append((neighbor, path + [neighbor]))
    return []

def run_dijkstra(start, goal):
    # Priority Queue: (total_cost, current_node, path)
    queue = [(0, start, [start])]
    seen = set()
    
    while queue:
        cost, current, path = heapq.heappop(queue)
        
        if current in seen: 
            continue
        seen.add(current)
        
        if current == goal:
            return path
            
        for neighbor, weight in get_neighbors(current).items():
            if neighbor not in seen:
                heapq.heappush(queue, (cost + weight, neighbor, path + [neighbor]))
    return []