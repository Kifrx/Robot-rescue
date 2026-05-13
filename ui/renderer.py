import pygame
from settings import *
from core.graph_data import nodes, edges

def draw_graph(screen, font):
    drawn_edges = set()
    
    for node, neighbors in edges.items():
        x1, y1 = nodes[node]
        for neighbor, weight in neighbors.items():
            edge_tuple = tuple(sorted((node, neighbor)))
            
            if edge_tuple not in drawn_edges:
                x2, y2 = nodes[neighbor]
                pygame.draw.line(screen, GRAY, (x1, y1), (x2, y2), 4)
                
                mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
                weight_text = font.render(str(weight), True, RED)
                text_rect = weight_text.get_rect(center=(mid_x, mid_y))
                
                pygame.draw.rect(screen, WHITE, text_rect)
                screen.blit(weight_text, text_rect)
                drawn_edges.add(edge_tuple)

    for node, pos in nodes.items():
        pygame.draw.circle(screen, BLACK, pos, 22)
        pygame.draw.circle(screen, WHITE, pos, 19) 
        
        node_text = font.render(str(node), True, BLACK)
        screen.blit(node_text, node_text.get_rect(center=pos))

def draw_animated_path(screen, path, anim_index, robot_pos):
    if not path:
        return
        
    for i in range(anim_index):
        p1 = nodes[path[i]]
        p2 = nodes[path[i+1]]
        pygame.draw.line(screen, GREEN, p1, p2, 6)
    
    if anim_index < len(path) - 1:
        p1 = nodes[path[anim_index]]
        pygame.draw.line(screen, GREEN, p1, robot_pos, 6)