import random

nodes = {}
edges = {}

# 1. Generate 36 Nodes 
node_id = 0
for row in range(6):
    for col in range(6):
        
        x = 80 + (col * 125)
        y = 130 + (row * 85)
        nodes[node_id] = (x, y)
        edges[node_id] = {}
        node_id += 1

# 2. Generate Edges 
random.seed(42)  

for i in range(36):
    row = i // 6
    col = i % 6
    
  
    if col < 5:
        weight = random.choice([5, 10, 15, 20, 25])
        edges[i][i+1] = weight
        edges[i+1][i] = weight
        
    if row < 5:
        weight = random.choice([5, 10, 15, 20, 25])
        edges[i][i+6] = weight
        edges[i+6][i] = weight
        
    if row < 5 and col < 5 and random.random() > 0.7:
        weight = random.choice([15, 30])
        edges[i][i+7] = weight
        edges[i+7][i] = weight