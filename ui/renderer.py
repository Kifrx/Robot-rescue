import pygame
from settings import *
from core.graph_data import nodes, edges

# BACKGROUND
def draw_background(screen):
    # Gradient background
    for y in range(screen.get_height()):
        color = 255 - int(80 * (y / screen.get_height()))
        pygame.draw.line(screen, (color, color, color), (0, y), (screen.get_width(), y))

# DRAW GRAPH
def draw_graph(screen, font, blocked_nodes=None):
    if blocked_nodes is None:
        blocked_nodes = set()

    drawn_edges = set()

    # DRAW EDGES
    for node, neighbors in edges.items():
        x1, y1 = nodes[node]

        for neighbor, weight in neighbors.items():
            edge_tuple = tuple(sorted((node, neighbor)))

            if edge_tuple not in drawn_edges:
                x2, y2 = nodes[neighbor]

                # Garis edge
                pygame.draw.line(screen, (180, 180, 180), (x1, y1), (x2, y2), 2)

                # Weight label
                mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
                weight_text = font.render(str(weight), True, RED)
                text_rect = weight_text.get_rect(center=(mid_x, mid_y))

                bg_rect = text_rect.inflate(10, 6)
                pygame.draw.rect(screen, (240, 240, 240), bg_rect, border_radius=6)
                pygame.draw.rect(screen, (200, 200, 200), bg_rect, 1, border_radius=6)

                screen.blit(weight_text, text_rect)

                drawn_edges.add(edge_tuple)

    # DRAW NODES
    for node, pos in nodes.items():
        x, y = pos

        # Warna node
        if node in blocked_nodes:
            main_color = (30, 30, 30)
            text_color = (255, 255, 255)
        else:
            main_color = (100, 200, 255)
            text_color = (0, 0, 0)

        # Shadow
        pygame.draw.circle(screen, (150, 150, 150), (x + 3, y + 3), 24)

        # Border
        pygame.draw.circle(screen, (30, 30, 30), pos, 24)

        # Fill
        pygame.draw.circle(screen, main_color, pos, 20)

        # Label
        node_text = font.render(str(node), True, text_color)
        screen.blit(node_text, node_text.get_rect(center=pos))

# DRAW PATH ANIMATION
def draw_animated_path(screen, path, anim_index, robot_pos):
    if not path:
        return

    # Path yang sudah dilewati
    for i in range(anim_index):
        p1 = nodes[path[i]]
        p2 = nodes[path[i + 1]]

        pygame.draw.line(screen, (0, 255, 0), p1, p2, 8)
        pygame.draw.line(screen, (0, 150, 0), p1, p2, 4)

    # Path yang sedang berjalan
    if anim_index < len(path) - 1:
        p1 = nodes[path[anim_index]]
        pygame.draw.line(screen, (0, 255, 0), p1, robot_pos, 6)
